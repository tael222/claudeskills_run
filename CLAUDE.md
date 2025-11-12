# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Claude Skills Run**은 Claude Code의 커스텀 스킬을 테스트하고 다양한 자동화 워크플로우를 추적/관리하기 위한 하이브리드 플랫폼입니다.

### Architecture

이 프로젝트는 **하이브리드 아키텍처**를 사용합니다:
- **Backend**: Python + FastAPI (비동기 REST API)
- **CLI**: Typer (명령줄 도구)
- **Frontend**: React + TypeScript (웹 대시보드)
- **Database**: SQLite + SQLAlchemy (워크플로우 추적)
- **AI Integration**: Anthropic SDK (Claude API)

### Core Functionality

1. **프로젝트 생성 자동화** (`src/workflows/project_gen.py`)
   - Flutter, Next.js, Python 등 다양한 프레임워크 지원
   - Clean Architecture 기반 템플릿

2. **코드 변경 추적** (`src/workflows/code_tracker.py`)
   - Git 커밋 기록 분석
   - 자동 변경사항 문서화

3. **AI 검증 루프** (`src/workflows/ai_verifier.py`)
   - Claude를 활용한 코드 검증
   - 계획 → 구현 → 검증 → 개선 사이클

4. **콘텐츠 생성** (`src/workflows/content_gen.py`)
   - 문서, 이미지, 마크다운 자동 생성

## Development Commands

### Setup

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치 (개발 도구 포함)
pip install -e ".[dev]"

# 환경 변수 설정
cp .env.example .env
# .env 파일에서 ANTHROPIC_API_KEY 설정 필요

# 프로젝트 초기화
claudeskills init
```

### Running Services

```bash
# CLI로 웹 서버 시작
claudeskills server start
# 또는 개발 모드 (auto-reload)
claudeskills server dev

# Uvicorn으로 직접 실행
uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000

# Frontend 개발 서버 (별도 터미널)
cd frontend
npm install  # 최초 1회
npm run dev
```

### Testing

```bash
# 전체 테스트 실행
pytest

# 특정 파일 테스트
pytest tests/test_workflows.py

# 커버리지 포함
pytest --cov=src --cov-report=html

# 단일 테스트 함수
pytest tests/test_workflows.py::test_project_generation -v
```

### Code Quality

```bash
# 자동 포맷팅
black src tests

# 린팅
ruff check src tests

# 자동 수정 가능한 린트 에러 수정
ruff check --fix src tests

# 타입 체크
mypy src
```

## Project Structure

```
claudeskills_run/
├── src/
│   ├── cli/              # Typer CLI 도구
│   │   ├── main.py       # CLI 진입점
│   │   └── commands/     # 명령어 모듈들
│   │       ├── init.py      # 프로젝트 초기화
│   │       ├── create.py    # 프로젝트 생성
│   │       ├── workflow.py  # 워크플로우 관리
│   │       ├── skills.py    # 스킬 관리
│   │       └── server.py    # 서버 관리
│   ├── api/              # FastAPI REST API
│   │   ├── app.py        # FastAPI 앱 (lifespan 이벤트 포함)
│   │   ├── routes/       # API 라우터들
│   │   └── models/       # Pydantic 모델들
│   ├── skills/           # Claude Skills 통합
│   │   ├── manager.py    # 스킬 로드/관리
│   │   └── executor.py   # 스킬 실행 엔진
│   ├── workflows/        # 워크플로우 엔진
│   │   ├── project_gen.py    # 프로젝트 생성 워크플로우
│   │   ├── code_tracker.py   # 코드 추적 워크플로우
│   │   ├── ai_verifier.py    # AI 검증 워크플로우
│   │   └── content_gen.py    # 콘텐츠 생성 워크플로우
│   └── core/             # 공통 모듈
│       ├── config.py     # 설정 관리 (Pydantic Settings)
│       ├── database.py   # DB 세션 관리 (sync/async 모두 지원)
│       └── logger.py     # Rich 로깅 설정
├── frontend/             # React + TypeScript
│   ├── src/
│   │   ├── components/   # React 컴포넌트
│   │   ├── pages/        # 페이지 컴포넌트
│   │   ├── services/     # API 클라이언트
│   │   └── hooks/        # 커스텀 훅
│   └── package.json
├── skills/               # 커스텀 Claude Skills 저장소
├── tests/                # 테스트 파일
├── docs/                 # 추가 문서
├── pyproject.toml        # Python 프로젝트 설정
└── .env                  # 환경 변수 (gitignore)
```

## Key Design Patterns

### Async/Sync Duality

데이터베이스 접근이 **두 가지 방식**으로 제공됩니다:
- **Async** (`get_async_db`): FastAPI 엔드포인트에서 사용
- **Sync** (`get_sync_db`): CLI 명령어에서 사용

예시:
```python
# FastAPI (async)
@router.get("/workflows")
async def get_workflows(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Workflow))
    return result.scalars().all()

# CLI (sync)
def list_workflows():
    db = next(get_sync_db())
    result = db.execute(select(Workflow))
    return result.scalars().all()
```

### Configuration Management

모든 설정은 `src/core/config.py`의 `Settings` 클래스에서 관리됩니다:
- Pydantic Settings 사용 (타입 안정성)
- `.env` 파일에서 자동 로드
- 환경 변수 오버라이드 가능

새 설정 추가 시:
1. `Settings` 클래스에 필드 추가
2. `.env.example`에 예시 값 추가
3. 필요시 `@property`로 계산된 값 제공

### Workflow System

워크플로우는 `src/workflows/`에 독립 모듈로 구현:
- 각 워크플로우는 실행 상태를 DB에 저장
- 비동기 실행 지원 (Celery 또는 asyncio)
- 중단/재개 가능한 체크포인트 시스템

### Skills Integration

bear2u/my-skills의 스킬들을 Python으로 재구현:
- `skills/` 디렉토리에 각 스킬의 메타데이터 저장
- `src/skills/manager.py`가 스킬 로드/등록 담당
- `src/skills/executor.py`가 Claude API 호출 및 실행

## API Endpoints

### Health Checks
- `GET /api/health` - 기본 헬스체크
- `GET /api/health/db` - 데이터베이스 연결 확인

### Workflows (미구현, 향후 추가)
- `GET /api/workflows` - 워크플로우 목록
- `POST /api/workflows/{name}/run` - 워크플로우 실행
- `GET /api/workflows/{id}/status` - 실행 상태 조회

### Skills (미구현, 향후 추가)
- `GET /api/skills` - 스킬 목록
- `GET /api/skills/{name}` - 스킬 상세 정보
- `POST /api/skills/{name}/execute` - 스킬 실행

## CLI Commands

### 프로젝트 관리
```bash
claudeskills init              # 프로젝트 초기화
claudeskills version           # 버전 정보
```

### 프로젝트 생성
```bash
claudeskills create nextjs --name my-app
claudeskills create flutter --name my_app --template clean-arch
```

### 워크플로우
```bash
claudeskills workflow list                    # 목록
claudeskills workflow run code-tracker        # 실행
claudeskills workflow status <workflow-id>    # 상태
```

### 스킬 관리
```bash
claudeskills skills list              # 목록
claudeskills skills info <name>       # 상세 정보
claudeskills skills install <source>  # 설치
```

### 서버
```bash
claudeskills server start             # 서버 시작
claudeskills server dev               # 개발 모드
```

## Database Models

데이터베이스 모델은 `src/api/models/`에 정의 (향후 구현):

**Workflow** - 워크플로우 실행 기록
- id, name, status, started_at, completed_at
- parameters (JSON), result (JSON), error

**Skill** - 스킬 메타데이터
- id, name, description, version
- config (JSON), enabled

**Project** - 생성된 프로젝트 추적
- id, name, type, path, created_at
- metadata (JSON)

## Environment Variables

`.env` 파일에서 설정 (`.env.example` 참조):

**필수:**
- `ANTHROPIC_API_KEY` - Claude API 키

**선택:**
- `DATABASE_URL` - 데이터베이스 경로 (기본: sqlite:///./claudeskills.db)
- `API_HOST`, `API_PORT` - 서버 설정
- `LOG_LEVEL` - 로그 레벨 (DEBUG, INFO, WARNING, ERROR)
- `SKILLS_DIR` - 스킬 디렉토리 경로

## Workflow Implementation Guide

새 워크플로우 추가 시:

1. `src/workflows/`에 모듈 생성
2. 워크플로우 클래스 정의:
   ```python
   class MyWorkflow:
       def __init__(self, db: Session):
           self.db = db

       async def execute(self, params: dict) -> dict:
           # 구현
           pass
   ```
3. `src/cli/commands/workflow.py`에 명령어 추가
4. `src/api/routes/workflows.py`에 API 엔드포인트 추가
5. 테스트 작성 (`tests/test_workflows.py`)

## Skill Development

bear2u/my-skills 스킬을 Python으로 포팅 시:

1. `skills/<skill-name>/` 디렉토리 생성
2. `skill.json` 메타데이터 파일 작성
3. `src/skills/<skill_name>.py`에 로직 구현
4. Claude API 프롬프트는 `skills/<skill-name>/prompts/` 저장
5. 테스트 추가

## Frontend Development

React + TypeScript frontend는 `frontend/` 디렉토리에 위치:
- Vite 빌드 시스템
- TailwindCSS 스타일링
- Axios로 백엔드 API 호출
- React Query로 데이터 페칭

Frontend 개발 시:
```bash
cd frontend
npm run dev       # 개발 서버
npm run build     # 프로덕션 빌드
npm run preview   # 빌드 미리보기
```

## Logging

Rich 라이브러리 사용:
- 콘솔: 컬러풀한 출력 + 트레이스백
- 파일: `logs/app.log`에 상세 로그 저장

로거 사용:
```python
from src.core.logger import logger

logger.info("정보 메시지")
logger.warning("경고 메시지")
logger.error("에러 메시지")
```

## References

- **bear2u/my-skills**: https://github.com/bear2u/my-skills
  - 이 프로젝트의 스킬 시스템 참조 원본
  - Flutter-init, Next.js-init 등 스킬 구조 참고

- **Claude Code Documentation**: https://docs.claude.com/en/docs/claude-code
  - 스킬 작성 가이드
  - API 사용법
