FROM python:3.11-slim

WORKDIR /app

COPY Services/django_app ./django_app
COPY Services/FastApi ./FastApi

RUN pip install --no-cache-dir -r ./django_app/requirements.txt
RUN pip install --no-cache-dir -r ./FastApi/requirements.txt

COPY start.sh .
RUN chmod +x start.sh

EXPOSE 8000
CMD ["/bin/bash", "start.sh"]
