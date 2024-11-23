# 가상환경 생성
uv venv

# 가상환경 활성화
.\.venv\Scripts\Activate.ps1

# 기본 의존성 설치
uv pip install -e .

# 개발 의존성 설치
uv pip install -e ".[dev]"

# 개발 도구 설정
pre-commit install 