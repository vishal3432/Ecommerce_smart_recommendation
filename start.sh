#!/bin/bash

echo "Starting Ecommerce Smart Recommendation System on Render..."

# Start FastAPI in the background on internal port 8001
echo "Starting FastAPI ML service on http://127.0.0.1:8001 ..."
cd /app/Services/fastapi_service
uvicorn main:app --host 127.0.0.1 --port 8001 &

# Give FastAPI a few seconds to fully start
sleep 8

# Start Django as the main public service using Render's $PORT
echo "Starting Django on port $PORT ..."
cd /app/Services/django_app

# Run migrations and collect static files
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

# Start Django
python manage.py runserver 0.0.0.0:$PORT
