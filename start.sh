#!/bin/bash

echo "🚀 Starting Ecommerce Smart Recommendation System on Render..."

# ====================== FastAPI Service ======================
echo "Starting FastAPI ML service on http://127.0.0.1:8001 ..."
cd /app/Services/FastApi

pip install --no-cache-dir -r requirements.txt || true

uvicorn main:app --host 127.0.0.1 --port 8001 &

sleep 10

# ====================== Django Main App ======================
echo "Starting Django on port $PORT ..."
cd /app/Services/django_app

python manage.py migrate --noinput || echo "⚠️ Migration skipped"
python manage.py collectstatic --noinput --clear || echo "⚠️ Collectstatic skipped"

echo "✅ Starting Django server on port $PORT..."
exec python manage.py runserver 0.0.0.0:$PORT
