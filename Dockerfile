# syntax=docker/dockerfile:1.7
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install Python deps first (better layer caching)
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# ENV=production switches main.py to BOT_TOKEN_PROD.
ENV ENV=production
# /health endpoint exposed alongside the Discord WebSocket connection.
EXPOSE 8080

CMD ["python", "main.py"]
