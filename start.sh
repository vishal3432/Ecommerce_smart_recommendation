#!/bin/bash

echo "Creating superuser..."

export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@gmail.com
export DJANGO_SUPERUSER_PASSWORD=admin123

cd django_app
python manage.py createsuperuser --noinput || echo "Superuser already exists"
cd ..

echo "🚀 Starting Ecommerce System..."

PORT=${PORT:-8000}

# ================= FastAPI =================
echo "⚡ Starting FastAPI..."

cd FastApi

uvicorn main:app --host 0.0.0.0 --port 8001 &

cd ..

sleep 5

# ================= Django =================
echo "🌐 Starting Django..."

cd django_app

python manage.py migrate --noinput || echo "Migration skipped"
python manage.py collectstatic --noinput --clear || echo "Collectstatic skipped"

echo "✅ Running Django with Gunicorn on port $PORT..."

exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
