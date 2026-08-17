# Student Management API

A FastAPI-based REST API for managing students, with JWT authentication and role-based access control (ADMIN / STUDENT).

## Tech Stack
- FastAPI
- SQLAlchemy (SQLite for local dev — swappable to PostgreSQL/MySQL via `DATABASE_URL`)
- Pydantic / pydantic-settings
- OAuth2 + JWT (python-jose)
- Passlib (bcrypt) for password hashing
- Pytest for automated testing

## Project Setup

1. Clone the repo and enter the project folder.
2. Create and activate a virtual environment:
    python -m venv venv
    venv\Scripts\Activate.ps1 
3. Install dependencies:
    pip install -r requirements.txt
4. Create a `.env` file (see below) — never commit this file.
5. Run the server:
    uvicorn app.main:app --reload
6. Open interactive docs: `http://127.0.0.1:8000/docs`

## Database Configuration

Set in `.env`:
  DATABASE_URL=sqlite:///./student_management.db
  SECRET_KEY=<a long random string>
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=30

Generate a secret key with:
    python -c "import secrets; print(secrets.token_hex(32))"

Tables are created automatically on first run via `Base.metadata.create_all()`. To use PostgreSQL/MySQL instead, just change `DATABASE_URL`.

## Authentication Flow

1. `POST /auth/register` — create a user with a role (`ADMIN` or `STUDENT`). Password is hashed with bcrypt before storage.
2. `POST /auth/login` — OAuth2 password flow; returns a JWT `access_token` (expires per `ACCESS_TOKEN_EXPIRE_MINUTES`).
3. Protected routes require `Authorization: Bearer <token>`. The token is verified (signature + expiry) via a reusable `get_current_user` dependency, which also fetches the current user from the DB.
4. Role checks are enforced via a reusable `require_role(*roles)` dependency factory.

## API Endpoints

| Method | Endpoint | Auth Required | Roles |
|---|---|---|---|
| POST | /auth/register | No | — |
| POST | /auth/login | No | — |
| GET | /auth/me | Yes | Any |
| GET | /students/ | Yes | Any |
| GET | /students/{id} | Yes | Any |
| POST | /students/ | Yes | ADMIN only |
| PUT | /students/{id} | Yes | ADMIN (any record) or STUDENT (own linked record only) |
| DELETE | /students/{id} | Yes | ADMIN only |

## Admin vs Student Permissions

- **ADMIN**: full CRUD on all student records.
- **STUDENT**: can view all students, can update only their own linked student record (via `owner_id`), cannot create or delete, and receives `403 Forbidden` on any admin-only action.

## Running Tests
python -m pytest -v

Tests use an isolated in-memory SQLite database and cover registration, login (success/failure), token validation, and the full RBAC matrix (admin full access, student restricted access, cross-user update blocking).
