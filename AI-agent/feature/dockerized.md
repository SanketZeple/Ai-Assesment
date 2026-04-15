TASK:
Dockerize existing fullstack project.

CONTEXT:
Project already built:
- backend/ (FastAPI + Alembic)
- frontend/ (React)
- DB: PostgreSQL
- Redis (for async/queue)

GOAL:
Containerize app without changing business logic.

REQUIREMENTS:
- Backend Dockerfile (include Alembic support)
- Frontend Dockerfile
- docker-compose with ONLY:
  - backend
  - frontend
  - postgres
  - redis
- Ensure backend runs Alembic migrations on startup
- Proper service networking (use service names)
- Env-based config (.env)
- DB + Redis connection setup
- Volume for PostgreSQL persistence
- Dev-friendly setup (hot reload if possible)

CONSTRAINTS:
- Do NOT modify existing app logic
- Do NOT add extra services/tools
- Keep minimal, clean, production-ready
- Only use backend, frontend, postgres, redis

OUTPUT:
- backend/Dockerfile
- frontend/Dockerfile
- docker-compose.yml
- Alembic migration setup (entrypoint/start command)
- .env example
- Run commands