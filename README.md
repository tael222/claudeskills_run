# Claude Skills Run

Claude Skills를 활용한 자동화 워크플로우 추적 및 테스트 플랫폼

## 프로젝트 개요

이 프로젝트는 Claude Code의 커스텀 스킬을 테스트하고 다양한 자동화 워크플로우를 관리하기 위한 하이브리드 플랫폼입니다.

### 주요 기능

- **프로젝트 생성 자동화**: Flutter, Next.js 등 다양한 프레임워크 프로젝트 자동 생성
- **코드 변경 추적**: Git 커밋, 코드 리뷰, 변경사항 자동 문서화
- **AI 검증 루프**: Claude를 활용한 코드 검증 및 개선 프로세스
- **콘텐츠 생성**: 문서, 이미지, 마크다운 자동 생성
- **웹 대시보드**: 워크플로우 시각화 및 관리
- **CLI 도구**: 터미널에서 간편한 명령어 실행

## 기술 스택

### Backend
- Python 3.10+
- FastAPI (웹 API)
- Typer (CLI)
- SQLAlchemy (ORM)
- Anthropic SDK (Claude API)

### Frontend
- React 18+
- TypeScript
- Vite
- TailwindCSS

## 설치

### 필수 요구사항
- Python 3.10 이상
- Node.js 18 이상
- Git

### Backend 설치

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -e ".[dev]"

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 ANTHROPIC_API_KEY 설정
```

### Frontend 설치

```bash
cd frontend
npm install
```

## 사용법

### CLI 명령어

```bash
# 도움말
claudeskills --help

# 프로젝트 생성
claudeskills create --type nextjs --name my-app

# 워크플로우 실행
claudeskills workflow run --name code-review

# 스킬 목록
claudeskills skills list
```

### 웹 대시보드

```bash
# Backend 서버 시작
uvicorn src.api.app:app --reload

# Frontend 개발 서버 시작 (새 터미널)
cd frontend
npm run dev
```

웹 브라우저에서 http://localhost:3000 접속

## 프로젝트 구조

```
claudeskills_run/
├── src/
│   ├── cli/              # CLI 도구
│   ├── api/              # FastAPI 웹 API
│   ├── skills/           # Claude Skills 통합
│   ├── workflows/        # 워크플로우 엔진
│   └── core/             # 공통 유틸리티
├── frontend/             # React 프론트엔드
├── skills/               # 커스텀 스킬 모음
├── tests/                # 테스트
└── docs/                 # 문서
```

## 개발

### 테스트 실행

```bash
# 전체 테스트
pytest

# 커버리지 포함
pytest --cov=src --cov-report=html
```

### 코드 품질

```bash
# 포맷팅
black src tests

# 린팅
ruff check src tests

# 타입 체크
mypy src
```

## 라이선스

MIT License

## 참고 자료

- [Claude Code 문서](https://docs.claude.com/en/docs/claude-code)
- [bear2u/my-skills](https://github.com/bear2u/my-skills) - 참고한 스킬 저장소
