# Hennepin – Dockerized Dev Setup

This repo contains a Django + DRF API. The project is containerized with Docker so you can spin it up quickly with a MySQL database.

## Prereqs

- Docker and Docker Compose v2

## Quick start

1. Configure ports in your .env (required before build/up):

   The docker-compose file reads host ports from the project `.env` file (Compose uses this for variable substitution):

   - `WEB_PORT` — host port for the Django app (default 8000)
   - `DB_PORT` — host port to expose MySQL for tools like DBeaver (default 3307)

   Example `.env` additions:

   ```env
   WEB_PORT=8000
   DB_PORT=3308
   ```

   Pick values that don’t conflict with anything already listening on your machine.

2. Build and start the stack:

   ```sh
   docker compose up --build
   ```

   - Web API: http://localhost:${WEB_PORT}/
   - MySQL for GUI clients (e.g., DBeaver): localhost:${DB_PORT}
   - The container will wait for MySQL, run migrations, then start the Django dev server.

3. Stop the stack:

   ```sh
   docker compose down
   ```

   Add `-v` to remove the MySQL volume if you want a clean DB:

   ```sh
   docker compose down -v
   ```

### Connect with DBeaver (or similar)

Use the MySQL driver with these settings (from `.env`):

- Host: `localhost`
- Port: `${DB_PORT}` (e.g., 3308)
- Database: `${MYSQL_DB}` (default `hennepin`)
- User: `${MYSQL_USER}` (default `hennepin_user`)
- Password: `${MYSQL_PASSWORD}` (default `password`)

## Create a user (temporary, pre-frontend)

Until the frontend is built, you can create users via the API (recommended for normal users) or via Django management commands (useful for a superuser/admin).

### Option A — Create a user via API and get tokens

Replace `8000` with your `WEB_PORT` if you changed it.

1) Register a new user (returns the created user and JWT tokens):

```sh
curl -X POST http://localhost:8000/api/auth/register/ \
   -H "Content-Type: application/json" \
   -d '{
      "username": "alice",
      "email": "alice@example.com",
      "password": "Str0ng!Pass123",
      "password2": "Str0ng!Pass123"
   }'
```

2) Or, if you already have a user, obtain a JWT access token:

```sh
curl -X POST http://localhost:8000/api/token/ \
   -H "Content-Type: application/json" \
   -d '{"username":"alice","password":"Str0ng!Pass123"}'
```

3) Use the access token to call protected endpoints (example: create a community):

```sh
curl -X POST http://localhost:8000/api/communities/ \
   -H "Authorization: Bearer <ACCESS_TOKEN>" \
   -H "Content-Type: application/json" \
   -d '{"name":"TestCommunity","description":"A test community"}'
```

### Option B — Create a Django superuser (admin)

Interactive (you'll be prompted for username/email/password):

```sh
docker compose exec web python manage.py createsuperuser
```

You can then log in (e.g., Django admin if enabled) and use these credentials for testing.

## Running tests locally

Tests default to the configured DB. To run against SQLite without MySQL, set:

```sh
USE_SQLITE=1 pytest -q
```
