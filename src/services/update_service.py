import requests
import os
import sys
import tempfile
import zipfile
from packaging import version
from config.version import VERSION, GITHUB_REPO
from dotenv import load_dotenv
import subprocess
import traceback
import shutil
import time
import re

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
        temp_dir = None
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
            
            # 임시 디렉토리 생성
            temp_dir = tempfile.mkdtemp()
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
            result = self._perform_update(temp_dir)
            return result
                
        except Exception as e:
            print(f"업데이트 설치 중 오류 발생: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"응답 내용: {e.response.text}")
            return False
        finally:
            # 업데이트 완료 후 임시 디렉토리 정리
            if temp_dir and os.path.exists(temp_dir):
                try:
                    time.sleep(5)  # 업데이트 스크립트가 파일을 사용할 시간을 줌
                    shutil.rmtree(temp_dir)
                except:
                    pass
    
    def _perform_update(self, update_dir):
        """실제 업데이트 수행"""
        try:
            # 현재 실행 파일 경로
            current_exe = sys.executable
            
            # 업데이트 스크립트 생성
            update_script = self._create_update_script(current_exe, update_dir)
            
            # 업데이트 스크립트 실행
            process = subprocess.Popen(
                [sys.executable, update_script],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
            # 스크립트가 시작될 때까지 잠시 대기
            time.sleep(2)
            
            # 프로세스가 시작되었는지 확인
            if process.poll() is None:
                print("업데이트 스크립트가 성공적으로 시작되었습니다.")
                sys.exit(0)  # 현재 프로그램 종료
            else:
                print("업데이트 스크립트 시작 실패")
                return False
                
        except Exception as e:
            print(f"업데이트 스크립트 실행 중 오류 발생: {e}")
            traceback.print_exc()
            return False
    
    def _create_update_script(self, current_exe, update_dir):
        """업데이트 스크립트 생성"""
        # 경로의 백슬래시를 이스케이프하거나 정방향 슬래시로 변환
        safe_update_dir = update_dir.replace('\\', '/')
        safe_current_exe = current_exe.replace('\\', '/')
        
        script_content = '''# -*- coding: utf-8 -*-
import os
import shutil
import time
import subprocess
import sys
import traceback
import re

def update_version_file(target_dir, latest_version):
    """version.py 파일의 버전 정보 업데이트"""
    version_file = os.path.join(target_dir, 'src', 'config', 'version.py')
    if os.path.exists(version_file):
        with open(version_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # VERSION 변수 업데이트
        new_content = re.sub(
            r'VERSION = "[^"]+"',
            f'VERSION = "{{latest_version}}"',
            content
        )
        
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"버전 정보를 {{latest_version}}로 업데이트했습니다.")

def main():
    try:
        print("업데이트 설치를 시작합니다...")
        # 원본 프로그램이 종료될 때까지 대기
        time.sleep(2)

        # 파일 교체
        source_dir = r"''' + safe_update_dir + '''"
        target_dir = os.path.dirname(r"''' + safe_current_exe + '''")

        # 압축 해제된 첫 번째 디렉토리 찾기 (GitHub 압축 파일 구조)
        subdirs = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
        if subdirs:
            source_dir = os.path.join(source_dir, subdirs[0])

        print(f"파일 복사 중... (소스: {{source_dir}})")
        
        # src 디렉토리 찾기
        src_dir = os.path.join(source_dir, 'src')
        if os.path.exists(src_dir):
            source_dir = src_dir
            
        # 파일 복사
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith('.py'):
                    source_path = os.path.join(root, file)
                    relative_path = os.path.relpath(source_path, source_dir)
                    target_path = os.path.join(target_dir, 'src', relative_path)
                    
                    print(f"복사 중: {{relative_path}}")
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.copy2(source_path, target_path)

        # version.py 파일 업데이트
        version_file = os.path.join(source_dir, 'config', 'version.py')
        if os.path.exists(version_file):
            with open(version_file, 'r', encoding='utf-8') as f:
                content = f.read()
                version_match = re.search(r'VERSION = "([^"]+)"', content)
                if version_match:
                    latest_version = version_match.group(1)
                    update_version_file(target_dir, latest_version)

        print("업데이트 완료. 프로그램을 재시작합니다...")
        
        # 새 버전 실행
        python_exe = sys.executable
        main_script = os.path.join(target_dir, "src", "main.py")
        
        # 프로그램 재시작
        process = subprocess.Popen(
            [python_exe, main_script],
            cwd=target_dir,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        
        # 프로세스가 시작되었는지 확인
        time.sleep(2)
        if process.poll() is None:
            print("프로그램이 성공적으로 재시작되었습니다.")
            time.sleep(1)
        else:
            print("프로그램 시작 실패")
            input("계속하려면 아무 키나 누르세요...")
            
    except Exception as e:
        print(f"업데이트 중 오류 발생: {{e}}")
        print("상세 오류:")
        traceback.print_exc()
        input("계속하려면 아무 키나 누르세요...")

if __name__ == "__main__":
    main()
'''
        
        script_path = os.path.join(tempfile.gettempdir(), 'update_script.py')
        # UTF-8 인코딩으로 파일 작성
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        return script_path 