FROM python:3.11-slim

WORKDIR /app

# Copy both services
COPY Services/django_app ./django_app
COPY Services/FastApi ./FastApi

# Install deps
RUN pip install --no-cache-dir -r ./django_app/requirements.txt
RUN pip install --no-cache-dir -r ./fastApi/requirements.txt

# Copy start script
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 8000
CMD ["./start.sh"]
