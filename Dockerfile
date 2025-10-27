# syntax=docker/dockerfile:1

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for mysqlclient and utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps via Pipenv using the lockfile for reproducibility
COPY Pipfile Pipfile.lock /app/
RUN pip install --no-cache-dir pipenv && \
    PIPENV_NOSPIN=1 PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy

# Copy project
COPY . /app

# Ensure entrypoint is executable
RUN chmod +x /app/docker/entrypoint.sh

EXPOSE 8000

CMD ["/app/docker/entrypoint.sh"]
