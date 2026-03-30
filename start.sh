#!/bin/bash

echo "Starting Ecommerce Smart Recommendation System on Render..."

# === Start FastAPI in background (using correct folder: FastApi) ===
echo "Starting FastAPI ML service on http://127.0.0.1:8001 ..."
cd /app/Services/FastApi || { echo "FastApi folder not found!"; exit 1; }

pip install --no-cache-dir -r requirements.txt || true

uvicorn main:app --host 127.0.0.1 --port 8001 &

sleep 10

# === Start Django as the main public service ===
echo "Starting Django on port $PORT ..."
cd /app/Services/django_app || { echo "django_app folder not found!"; exit 1; }

python manage.py migrate --noinput || echo "Migration skipped or failed"
python manage.py collectstatic --noinput --clear || echo "Collectstatic skipped"

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:$PORT
