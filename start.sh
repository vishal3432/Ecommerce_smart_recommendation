#!/bin/bash

echo "Starting Ecommerce Smart Recommendation System on Render..."

# Try multiple possible FastAPI folder names
if [ -d "/app/Services/FastApi" ]; then
    FASTAPI_DIR="/app/Services/FastApi"
    echo "Using FastApi folder"
elif [ -d "/app/Services/fastapi_service" ]; then
    FASTAPI_DIR="/app/Services/fastapi_service"
    echo "Using fastapi_service folder"
else
    echo "No FastAPI folder found! Available folders:"
    ls -la /app/Services/
    exit 1
fi

echo "Starting FastAPI ML service on http://127.0.0.1:8001 ..."
cd "$FASTAPI_DIR"

pip install --no-cache-dir -r requirements.txt || true

uvicorn main:app --host 127.0.0.1 --port 8001 &

sleep 10

# Start Django
echo "Starting Django on port $PORT ..."
cd /app/Services/django_app || { echo "django_app folder not found!"; exit 1; }

python manage.py migrate --noinput || echo "Migration skipped"
python manage.py collectstatic --noinput --clear || echo "Collectstatic skipped"

echo "Starting Django server on port $PORT..."
exec python manage.py runserver 0.0.0.0:$PORT
python manage.py migrate --noinput || echo "Migration skipped or failed"
python manage.py collectstatic --noinput --clear || echo "Collectstatic skipped"

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:$PORT
