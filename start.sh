#!/bin/bash

# Start FastAPI recommendation service in background
cd /app/FastApi
uvicorn main:app --host 0.0.0.0 --port 8001 &

# Start Django using Railway's dynamic PORT
cd /app/django_app
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
