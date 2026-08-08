# Backend Service

This is the backend service for the Blog Platform.
It exposes a REST API using FastAPI, handles authentication, data persistence, and file uploads.

## Purpose

- API for user registration, login, and email verification
- Post and tag management
- File upload handling for post covers and avatars
- Database migrations using Alembic

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Redis
- Uvicorn

## Local development

### Requirements

- Python 3.12
- pip
- Docker / Docker Compose (recommended)

### Environment

Copy the example environment file and configure values:

```powershell
copy .env.example .env
```

Then edit `backend/.env` and set:

- `SECRET_KEY`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DATABASE_URL`
- `REDIS_URL`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `ALGORITHM`

### Run locally with Docker Compose

From the repository root:

```powershell
docker compose up -d --build backend postgres redis
```

The backend will be available internally at `http://backend:8000` and exposed through the proxy at `http://localhost:8080/api/`.

### Run locally without Docker

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Database migrations

Use Alembic to create and apply migrations:

```powershell
cd backend
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

## API Endpoints

### Auth

- `POST /api/auth/login` — authenticate user
- `POST /api/auth/verify` — verify email token
- `GET /api/auth/me` — current authenticated user

### Users

- `POST /api/users` — create new user

### Posts, uploads, and tags

The backend also exposes posts, upload, and tag routes under `/api/`. Check `backend/app/api/v1/` for the full set of routers.

## Important notes

- The backend enforces email verification before issuing login tokens.
- Uploaded files are served from `/uploads` through the backend and proxied by NGINX.
- `backend/Dockerfile` runs `alembic upgrade head` at startup to ensure schema migration.

## File structure

```text
backend/
├── alembic/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── requirements.txt
└── Dockerfile
```
