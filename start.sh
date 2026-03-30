#!/bin/bash

# Start FastAPI (Recommendation service) in background on internal port 8001
cd /app/FastApi
uvicorn main:app --host 0.0.0.0 --port 8001 &

# Start Django using Railway's dynamic PORT
cd /app/django_app
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
