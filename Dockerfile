FROM python:3.12-slim

WORKDIR /app

# System packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY pyproject.toml .
COPY src ./src

# Install dependencies
RUN pip install --no-cache-dir .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "src.app:create_app()"]