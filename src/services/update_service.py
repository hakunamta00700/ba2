import requests
import os
import sys
import tempfile
import zipfile
from packaging import version
from config.version import VERSION, GITHUB_REPO
from dotenv import load_dotenv

class UpdateService:
    def __init__(self):
        # .env 파일 로드
        load_dotenv()
        
        self.current_version = VERSION
        self.github_api_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases"
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        } if self.github_token else {}
        
    def check_for_updates(self):
        """최신 버전이 있는지 확인"""
        try:
            # 모든 릴리즈를 가져옴
            response = requests.get(self.github_api_url, headers=self.headers)
            response.raise_for_status()
            
            releases = response.json()
            if not releases:
                print("릴리즈를 찾을 수 없습니다.")
                return False
            
            # 가장 최신 릴리즈 찾기
            latest_release = releases[0]  # GitHub API는 최신 순으로 정렬됨
            latest_version = latest_release['tag_name'].lstrip('v')
            
            print(f"현재 버전: v{self.current_version}")
            print(f"최신 버전: v{latest_version}")
            
            current_ver = version.parse(self.current_version)
            latest_ver = version.parse(latest_version)
            
            if latest_ver > current_ver:
                print(f"새로운 버전이 있습니다: v{latest_version}")
                return True
            else:
                print(f"현재 최신 버전을 사용 중입니다: v{self.current_version}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"업데이트 확인 중 오류 발생: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"응답 내용: {e.response.text}")
            return False
    
    def download_and_install_update(self):
        """최신 버전 다운로드 및 설치"""
        try:
            response = requests.get(self.github_api_url, headers=self.headers)
            response.raise_for_status()
            
            releases = response.json()
            if not releases:
                print("다운로드할 릴리즈가 없습니다.")
                return False
            
            latest_release = releases[0]
            download_url = latest_release['zipball_url']
            
            print(f"다운로드 URL: {download_url}")
            
            # 임시 디렉토리에 다운로드
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, "update.zip")
                
                # 업데이트 파일 다운로드
                print("업데이트 파일 다운로드 중...")
                response = requests.get(download_url, headers=self.headers)
                response.raise_for_status()
                
                with open(zip_path, 'wb') as f:
                    f.write(response.content)
                
                # 압축 해제
                print("파일 압축 해제 중...")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # 실제 업데이트 수행
                print("업데이트 설치 중...")
                self._perform_update(temp_dir)
                
            return True
        except Exception as e:
            print(f"업데이트 설치 중 오류 발생: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"응답 내용: {e.response.text}")
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
        # 경로의 백슬래시를 이스케이프하거나 정방향 슬래시로 변환
        safe_update_dir = update_dir.replace('\\', '/')
        safe_current_exe = current_exe.replace('\\', '/')
        
        script_content = f'''# -*- coding: utf-8 -*-
import os
import shutil
import time

# 원본 프로그램이 종료될 때까지 대기
time.sleep(1)

# 파일 교체
source_dir = r"{safe_update_dir}"
target_dir = os.path.dirname(r"{safe_current_exe}")

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
os.startfile(r"{safe_current_exe}")
'''
        
        script_path = os.path.join(tempfile.gettempdir(), 'update_script.py')
        # UTF-8 인코딩으로 파일 작성
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        return script_path 