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
    && rm -rf /var/lib/apt/lists/*

# Install Python deps via Pipenv using the lockfile for reproducibility
RUN pip install --no-cache-dir pipenv
ENV PIPENV_NOSPIN=1
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy

# Copy project
COPY . /app

EXPOSE 8000

# Start Gunicorn directly. Use the $PORT provided by the platform (e.g. Fly).
# Use sh -c so environment variables like ${PORT} and ${WEB_CONCURRENCY} are expanded at runtime.
CMD ["sh", "-c", "gunicorn app.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${WEB_CONCURRENCY:-3} --log-level info"]
