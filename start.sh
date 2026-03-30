#!/bin/bash
set -e

# Start FastAPI in background
cd /app/FastApi
uvicorn main:app --host 0.0.0.0 --port 8001 &

# Start Django with explicit PORT handling
cd /app/django_app
echo "Starting Django on port $PORT"
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --log-level info
