#!/bin/bash

echo "Starting Ecommerce System"

# FastAPI 
echo "Starting FastAPI..."

cd Services/FastApi
uvicorn main:app --host 0.0.0.0 --port 8001 &

cd ../..

sleep 5

# Django
echo "Starting Django..."

cd Services/django_app

python manage.py migrate --noinput || echo "Migration skipped"
python manage.py collectstatic --noinput --clear || echo "Collectstatic skipped"

echo "Running Django with Gunicorn..."

exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
