#!/bin/sh
set -e

# Wait for MySQL if configured
if [ -n "$MYSQL_HOST" ]; then
  HOST="$MYSQL_HOST"
  PORT="${MYSQL_PORT:-3306}"
  echo "Waiting for database at ${HOST}:${PORT}..."
  until nc -z "$HOST" "$PORT"; do
    sleep 1
  done
  echo "Database is up."
fi

python manage.py migrate --noinput

exec python manage.py runserver 0.0.0.0:8000
