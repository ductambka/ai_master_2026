FROM python:3.11-slim

WORKDIR /app
COPY service ./service

EXPOSE 8080
USER  nobody
CMD ["python", "-m", "service", "--host", "0.0.0.0", "--port", "8080"]
