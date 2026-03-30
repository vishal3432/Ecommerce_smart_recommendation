#!/bin/bash

echo "Starting Ecommerce Smart Recommendation System on Render..."

# Start FastAPI (ML Recommendation Service) in background
echo "Starting FastAPI ML service on http://127.0.0.1:8001 ..."
cd Services/FastApi

# Install requirements
pip install --no-cache-dir -r requirements.txt || true

uvicorn main:app --host 127.0.0.1 --port 8001 &

# Wait for FastAPI to start properly
sleep 10

# Start Django as the main public service
echo "Starting Django on port $PORT ..."
cd Services/django_app

# Important Django commands
python manage.py migrate --noinput || echo "Migration skipped"
python manage.py collectstatic --noinput --clear || echo "Collectstatic skipped"

echo "✅ Django server starting on port $PORT..."
exec python manage.py runserver 0.0.0.0:$PORT
