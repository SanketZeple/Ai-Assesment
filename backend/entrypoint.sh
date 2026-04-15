#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL is up."

# Debug: Show DATABASE_URL (mask password)
echo "DATABASE_URL: $(echo $DATABASE_URL | sed 's/:[^:]*@/:****@/')"

# Run database migrations
echo "Running database migrations..."
python -m alembic upgrade head

# Start the application
echo "Starting application..."
if [ "$DEBUG" = "true" ]; then
    echo "Running in development mode with hot reload"
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Running in production mode"
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
fi