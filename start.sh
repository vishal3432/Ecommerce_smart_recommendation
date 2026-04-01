#!/bin/bash

set -e  # ❗ Stop on error

echo "🚀 Starting Ecommerce System..."

PORT=${PORT:-8000}
FASTAPI_PORT=8001

# ================= FastAPI =================
echo "⚡ Starting FastAPI..."

cd FastApi

# Run FastAPI in background with logs
uvicorn main:app --host 0.0.0.0 --port $FASTAPI_PORT &

FASTAPI_PID=$!

cd ..

sleep 3

# ================= Django =================
echo "🛠 Starting Django..."

cd django_app

# Migrate FIRST
echo "📦 Running migrations..."
python manage.py migrate --noinput || echo "Migration skipped"

# Collect static
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear || echo "Collectstatic skipped"

# Create/Update Superuser
echo "👤 Creating or updating superuser..."

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

username = "Vishal"
email = "vishal@gmail.com"
password = "Vishal@123"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superuser created")
else:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("Superuser updated")
EOF

echo "🌐 Running Django with Gunicorn on port $PORT..."

# Run Django in foreground (main process)
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT &

DJANGO_PID=$!

# ================= Monitor =================
echo "📡 Services running..."
echo "Django PID: $DJANGO_PID"
echo "FastAPI PID: $FASTAPI_PID"

# Wait for any process to exit
wait -n

echo "❌ One of the services stopped. Shutting down..."

kill -TERM $DJANGO_PID $FASTAPI_PID 2>/dev/null
