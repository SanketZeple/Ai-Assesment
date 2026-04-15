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
Set `DEBUG=true` in `backend/.env` to enable hot reload for backend code changes.

## Environment Variables
Key environment variables (see `backend/.env.example` for full list):
- `DATABASE_URL`: PostgreSQL connection string
- `LLM_API_KEY`: Your OpenAI API key
- `LLM_MODEL`: LLM model to use (default: gpt-3.5-turbo)
- `REDIS_URL`: Redis connection URL
- `VITE_API_BASE_URL`: Frontend API base URL
- `DEBUG`: Enable hot reload and debug mode (true/false)

## Troubleshooting
- If migrations fail, ensure PostgreSQL is running and accessible
- If frontend cannot connect to backend, check `VITE_API_BASE_URL` matches backend service name
- For hot reload issues, verify `DEBUG=true` is set in backend environment