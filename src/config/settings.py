import os
from dotenv import load_dotenv

# .env 파일 경로 계산
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
print(f"Loading .env from: {env_path}")

# .env 파일 로드
load_dotenv(env_path)

class Settings:
    # API 설정
    API_HOST = os.getenv('API_HOST', 'http://192.168.68.124')
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '5'))
    
    # 데이터베이스 설정
    DB_PATH = os.getenv('DB_PATH', 'local_data.txt')
    
    # 개발 모드 설정
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # 로깅 설정
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'scan_log.txt')

settings = Settings() 