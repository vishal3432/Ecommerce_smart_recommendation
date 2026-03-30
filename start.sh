#!/bin/bash
set -e

echo "Starting FastAPI on port 8001..."
cd /app/FastApi
uvicorn main:app --host 0.0.0.0 --port 8001 &

echo "Starting Django on Railway port $PORT..."
cd /app/django_app
exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT}" --log-level info
