# TODO List - Claude Skills Run

## 🎯 Current Sprint (Next Session)

### Priority 1: Workflow Execution API ⏳
- [ ] Add workflow execution endpoint to `src/api/routes/workflows.py`
  - [ ] `POST /api/workflows/{workflow_id}/execute` - Execute a workflow
  - [ ] `GET /api/workflows/{workflow_id}/logs` - Get execution logs
- [ ] Update Pydantic schemas with execution request/response
- [ ] Test execution with example workflows (echo, file_operations)
- [ ] Update API documentation

**Files to modify:**
- `src/api/routes/workflows.py`
- `src/api/models/schemas.py`

**Test command:**
```bash
# Create a workflow
curl -X POST http://localhost:8000/api/workflows \
  -H "Content-Type: application/json" \
  -d '{"name":"echo","description":"Test echo","parameters":{"message":"Hello"}}'

# Execute it (workflow_id from previous response)
curl -X POST http://localhost:8000/api/workflows/1/execute
```

---

### Priority 2: Claude Skills Integration 🤖
- [ ] Create skills module structure
  - [ ] `src/skills/manager.py` - Skills discovery and loading
  - [ ] `src/skills/executor.py` - Skills execution engine
  - [ ] `src/skills/claude_client.py` - Claude API integration
- [ ] Port 1-2 skills from bear2u/my-skills
  - [ ] Skill 1: `web-to-markdown` (simpler, useful)
  - [ ] Skill 2: `code-changelog` (more complex, demonstrates AI integration)
- [ ] Add skills execution API endpoints
- [ ] Test skills with Claude API

**Files to create:**
- `src/skills/manager.py`
- `src/skills/executor.py`
- `src/skills/claude_client.py`
- `skills/web-to-markdown/skill.json`
- `skills/code-changelog/skill.json`

**Environment:**
- Make sure `ANTHROPIC_API_KEY` is set in `.env`

---

### Priority 3: React Frontend 🎨
- [ ] Initialize React project with Vite + TypeScript
  ```bash
  cd frontend
  npm create vite@latest . -- --template react-ts
  npm install
  ```
- [ ] Install dependencies
  ```bash
  npm install axios @tanstack/react-query react-router-dom
  npm install -D tailwindcss postcss autoprefixer
  npx tailwindcss init -p
  ```
- [ ] Create basic layout
  - [ ] `src/App.tsx` - Main app with routing
  - [ ] `src/components/Layout.tsx` - Layout with sidebar
  - [ ] `src/pages/Dashboard.tsx` - Dashboard home
  - [ ] `src/pages/Workflows.tsx` - Workflows list
  - [ ] `src/pages/Skills.tsx` - Skills list
  - [ ] `src/pages/Projects.tsx` - Projects list
- [ ] Setup API client
  - [ ] `src/services/api.ts` - Axios instance
  - [ ] `src/services/workflows.ts` - Workflows API
  - [ ] `src/services/skills.ts` - Skills API
- [ ] Connect to backend API

**Files to create:**
- `frontend/src/App.tsx`
- `frontend/src/components/Layout.tsx`
- `frontend/src/pages/*`
- `frontend/src/services/*`
- `frontend/tailwind.config.js`

---

### Priority 4: Testing & Documentation ✅
- [ ] Write API tests
  - [ ] `tests/test_workflows.py` - Workflow CRUD and execution
  - [ ] `tests/test_skills.py` - Skills API
  - [ ] `tests/test_projects.py` - Projects API
- [ ] Update documentation
  - [ ] Add usage examples to README
  - [ ] Document workflow creation
  - [ ] Document skills development
- [ ] Add pre-commit hooks
  ```bash
  pre-commit install
  ```

**Test commands:**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_workflows.py -v

# Run with coverage
pytest --cov=src --cov-report=html
```

---

## 🔄 Backlog (Future Sessions)

### Advanced Features
- [ ] Workflow scheduling (cron-like)
- [ ] Workflow dependencies (DAG execution)
- [ ] Real-time logs with WebSocket
- [ ] Skill marketplace integration
- [ ] Docker containerization
- [ ] CI/CD with GitHub Actions

### UI Enhancements
- [ ] Dark mode
- [ ] Workflow visual editor
- [ ] Real-time status updates
- [ ] Charts and analytics

### Performance
- [ ] Add Redis for caching
- [ ] Background task queue (Celery)
- [ ] Database migrations with Alembic

---

## 📝 Notes for Next Session

### Quick Start Commands
```bash
# 1. Activate environment
cd /Users/hee/Documents/GitHub/claudeskills_run
source venv/bin/activate

# 2. Check current status
git status
git log --oneline -3

# 3. Start server (for testing)
claudeskills server start

# 4. Run tests
pytest
```

### Context for Claude
- **Main branch**: All code is in `main` branch
- **Database**: SQLite file at `./claudeskills.db`
- **Config**: Settings in `.env` file
- **Docs**: Auto-generated at http://localhost:8000/api/docs

### Bear2u Skills Reference
Clone for reference (optional):
```bash
cd ..
git clone https://github.com/bear2u/my-skills.git
cd claudeskills_run
```

---

## 🎉 Completed Tasks

- ✅ Project initialization (pyproject.toml, directory structure)
- ✅ Database models (Workflow, Skill, Project)
- ✅ REST API endpoints (CRUD for all models)
- ✅ Workflow execution engine (BaseWorkflow, WorkflowExecutor)
- ✅ Example workflows (Echo, FileOperations, DataProcessing)
- ✅ CLI tool with Typer
- ✅ Logging and configuration
- ✅ GitHub repository setup
- ✅ CLAUDE.md documentation
- ✅ Playwright integration for screenshots

**Last updated**: 2025-01-12
**Total commits**: 3
**GitHub**: https://github.com/tael222/claudeskills_run
