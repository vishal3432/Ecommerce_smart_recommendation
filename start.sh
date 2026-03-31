#!/bin/bash

echo "Starting Ecommerce System..."

PORT=${PORT:-8000}

# ================= FastAPI =================
echo "Starting FastAPI..."

cd FastApi
uvicorn main:app --host 0.0.0.0 --port 8001 &
cd ..

sleep 5

# ================= Django =================
echo "Starting Django..."

cd django_app

# Migrate FIRST
python manage.py migrate --noinput || echo "Migration skipped"

# Collect static
python manage.py collectstatic --noinput --clear || echo "Collectstatic skipped"

# Create/Update Superuser (AFTER migration)
echo "Creating or updating superuser..."

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

# Start server
echo "Running Django with Gunicorn on port $PORT..."

exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
