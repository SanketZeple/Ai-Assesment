# Dockerization Improvements Plan

## Current Status Assessment
The project already has Dockerization with:
- Backend Dockerfile (includes Alembic support via entrypoint)
- Frontend Dockerfile (multi-stage production build)
- docker-compose.yml with backend, frontend, postgres, redis
- Proper networking, volumes, health checks
- .env.example file

## Required Improvements per Requirements

### 1. Clean up docker-compose.yml
**Issue:** Contains commented nginx reverse proxy section (lines 82-95)
**Solution:** Remove commented section to keep minimal, clean compose file
**File:** `docker-compose.yml`
**Change:** Delete lines 82-95 (including comments)

### 2. Add hot reload for backend in development
**Issue:** Backend runs without hot reload, making development less friendly
**Solution:** Modify entrypoint.sh to conditionally add `--reload` flag when DEBUG=true
**File:** `backend/entrypoint.sh`
**Change:** Replace line 20 with conditional logic:
```bash
# Start the application
echo "Starting application..."
if [ "$DEBUG" = "true" ]; then
    echo "Running in development mode with hot reload"
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Running in production mode"
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
fi
```

### 3. Update .env.example with missing variables
**Issue:** Missing REDIS_URL and VITE_API_BASE_URL
**Solution:** Add these variables with appropriate defaults
**File:** `backend/.env.example`
**Change:** Add after existing variables:
```
# Redis
REDIS_URL=redis://localhost:6379/0

# Frontend
VITE_API_BASE_URL=http://localhost:8000
```

### 4. Create run commands documentation
**Issue:** Need clear run commands for Docker setup
**Solution:** Create a simple `RUN_COMMANDS.md` or update README
**File:** `RUN_COMMANDS.md` (new)
**Content:**
```markdown
# Docker Run Commands

## Quick Start
1. Copy environment file:
   ```bash
   cp backend/.env.example backend/.env
   ```
2. Set your LLM API key in `backend/.env`:
   ```
   LLM_API_KEY=your_openai_api_key_here
   ```
3. Start all services:
   ```bash
   docker-compose up -d
   ```
4. View logs:
   ```bash
   docker-compose logs -f
   ```

## Useful Commands
- Build images: `docker-compose build`
- Stop services: `docker-compose down`
- Stop and remove volumes: `docker-compose down -v`
- Restart backend only: `docker-compose restart backend`
- Check service status: `docker-compose ps`
- Run migrations manually: `docker-compose exec backend python -m alembic upgrade head`

## Access Services
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- PostgreSQL: localhost:5432 (user: postgres, password: postgres)
- Redis: localhost:6379

## Development Mode
Set `DEBUG=true` in `backend/.env` to enable hot reload.
```

## Validation Checklist
- [ ] docker-compose.yml contains only backend, frontend, postgres, redis (no commented sections)
- [ ] Backend entrypoint.sh supports hot reload when DEBUG=true
- [ ] .env.example includes REDIS_URL and VITE_API_BASE_URL
- [ ] Run commands documentation created
- [ ] All services start successfully with `docker-compose up -d`
- [ ] Alembic migrations run on backend startup
- [ ] Frontend health check passes
- [ ] Backend health check passes

## Implementation Order
1. Update docker-compose.yml
2. Update backend/entrypoint.sh
3. Update backend/.env.example
4. Create RUN_COMMANDS.md
5. Test the changes

## Notes
- No business logic changes required
- All changes are Docker/configuration only
- Maintains production-ready minimal setup
- Improves developer experience with hot reload