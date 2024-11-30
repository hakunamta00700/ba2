import os
import sys
import requests
import json
from pathlib import Path
import re
from dotenv import load_dotenv
import subprocess  # Git 명령어 실행을 위해 추가

# 프로젝트 루트 디렉토리 찾기
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# .env 파일 로드
load_dotenv(project_root / '.env')

from src.config.version import VERSION, GITHUB_REPO

class ReleaseManager:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        if not self.github_token:
            raise ValueError(
                "GitHub 토큰이 설정되지 않았습니다. "
                ".env 파일에 GITHUB_TOKEN을 설정하거나 "
                "환경변수로 설정해주세요."
            )
        
        self.api_url = f"https://api.github.com/repos/{GITHUB_REPO}"
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def create_git_tag(self, version_tag):
        """Git 태그 생성 및 푸시"""
        try:
            # 변경사항 커밋
            subprocess.run(['git', 'add', 'src/config/version.py'], check=True)
            subprocess.run(['git', 'commit', '-m', f'chore: bump version to v{version_tag}'], check=True)
            
            # 태그 생성
            tag_name = f'v{version_tag}'
            subprocess.run(['git', 'tag', '-a', tag_name, '-m', f'Release {tag_name}'], check=True)
            
            # 변경사항과 태그 푸시
            subprocess.run(['git', 'push'], check=True)
            subprocess.run(['git', 'push', 'origin', tag_name], check=True)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"Git 작업 중 오류 발생: {e}")
            return False

    def get_current_branch(self):
        """현재 Git 브랜치 이름 가져오기"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"브랜치 확인 중 오류 발생: {e}")
            return 'main'  # 기본값

    def create_release(self, version_tag, release_notes):
        """GitHub 릴리즈 생성"""
        # 먼저 Git 태그 생성
        if not self.create_git_tag(version_tag):
            return False

        # 현재 브랜치 확인
        current_branch = self.get_current_branch()
        
        url = f"{self.api_url}/releases"
        data = {
            'tag_name': f'v{version_tag}',
            'target_commitish': current_branch,  # 현재 브랜치 사용
            'name': f'Release v{version_tag}',
            'body': release_notes,
            'draft': False,
            'prerelease': False
        }

        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            print(f"릴리즈 v{version_tag}가 성공적으로 생성되었습니다!")
            return True
        else:
            print(f"릴리즈 생성 실패: {response.status_code}")
            print(response.json())
            return False

    def update_version_file(self, new_version):
        """version.py 파일 업데이트"""
        version_file = project_root / 'src' / 'config' / 'version.py'
        with open(version_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # VERSION 변수 업데이트
        new_content = re.sub(
            r'VERSION = "[^"]+"',
            f'VERSION = "{new_version}"',
            content
        )

        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

    def get_changes(self):
        """변경사항 입력 받기"""
        print("\n변경사항을 입력하세요 (입력 완료 후 빈 줄에서 Ctrl+D 또는 Ctrl+Z):")
        changes = []
        try:
            while True:
                line = input()
                if not line:
                    break
                changes.append(line)
        except EOFError:
            pass
        
        return "\n".join(changes)

def increment_version(version_str):
    """버전 번호 증가"""
    major, minor, patch = map(int, version_str.split('.'))
    return f"{major}.{minor}.{patch + 1}"

def main():
    try:
        release_manager = ReleaseManager()
        
        # 현재 버전 확인
        current_version = VERSION
        print(f"현재 버전: {current_version}")
        
        # 새 버전 번호 생성
        new_version = increment_version(current_version)
        print(f"새 버전: {new_version}")
        
        # 사용자 확인
        if input(f"버전 {new_version}으로 릴리즈를 생성하시겠습니까? (y/n): ").lower() != 'y':
            print("릴리즈가 취소되었습니다.")
            return
        
        # 변경사항 입력 받기
        release_notes = release_manager.get_changes()
        if not release_notes.strip():
            print("변경사항이 입력되지 않았습니다. 릴리즈를 취소합니다.")
            return
        
        # version.py 파일 업데이트
        release_manager.update_version_file(new_version)
        print("버전 파일이 업데이트되었습니다.")
        
        # GitHub 릴리즈 생성
        if release_manager.create_release(new_version, release_notes):
            print("릴리즈 프로세스가 완료되었습니다!")
        else:
            print("릴리즈 생성 중 오류가 발생했습니다.")
            
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main() 