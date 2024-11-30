import requests
import os
import sys
import tempfile
import zipfile
from packaging import version
from config.version import VERSION, GITHUB_REPO

class UpdateService:
    def __init__(self):
        self.current_version = VERSION
        self.github_api_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        
    def check_for_updates(self):
        """최신 버전이 있는지 확인"""
        try:
            response = requests.get(self.github_api_url)
            response.raise_for_status()
            
            latest_release = response.json()
            latest_version = latest_release['tag_name'].lstrip('v')
            
            return version.parse(latest_version) > version.parse(self.current_version)
        except Exception as e:
            print(f"업데이트 확인 중 오류 발생: {e}")
            return False
            
    def download_and_install_update(self):
        """최신 버전 다운로드 및 설치"""
        try:
            response = requests.get(self.github_api_url)
            response.raise_for_status()
            
            latest_release = response.json()
            download_url = latest_release['zipball_url']
            
            # 임시 디렉토리에 다운로드
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, "update.zip")
                
                # 업데이트 파일 다운로드
                response = requests.get(download_url)
                with open(zip_path, 'wb') as f:
                    f.write(response.content)
                
                # 압축 해제
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # 여기서 실제 업데이트 프로세스 실행
                # (현재 실행 파일을 종료하고 새 버전으로 교체)
                self._perform_update(temp_dir)
                
            return True
        except Exception as e:
            print(f"업데이트 설치 중 오류 발생: {e}")
            return False
    
    def _perform_update(self, update_dir):
        """실제 업데이트 수행"""
        # 현재 실행 파일 경로
        current_exe = sys.executable
        
        # 업데이트 스크립트 생성
        update_script = self._create_update_script(current_exe, update_dir)
        
        # 업데이트 스크립트 실행
        os.system(f'start /B python "{update_script}"')
        sys.exit(0)
    
    def _create_update_script(self, current_exe, update_dir):
        """업데이트 스크립트 생성"""
        script_content = f'''
import os
import shutil
import time

# 원본 프로그램이 종료될 때까지 대기
time.sleep(1)

# 파일 교체
source_dir = "{update_dir}"
target_dir = os.path.dirname("{current_exe}")

# 파일 복사
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.endswith('.py'):
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, source_dir)
            target_path = os.path.join(target_dir, relative_path)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.copy2(source_path, target_path)

# 새 버전 실행
os.startfile("{current_exe}")
'''
        
        script_path = os.path.join(tempfile.gettempdir(), 'update_script.py')
        with open(script_path, 'w') as f:
            f.write(script_content)
        return script_path 