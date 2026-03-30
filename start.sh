#!/bin/bash

# Start FastAPI in background on internal port 8001
cd /app/fastapi_service
uvicorn main:app --host 0.0.0.0 --port 8001 &

# Start Django on Railway's $PORT
cd /app/django_app
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
