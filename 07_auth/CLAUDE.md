# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI authentication API implementing JWT-based user authentication with refresh tokens. Uses SQLModel ORM with PostgreSQL, Argon2 password hashing, and HTTP-only cookies for secure token storage.

## Commands

```bash
# Run development server
uv run fastapi dev main.py

# Run production server
uv run fastapi run main.py

# Install dependencies
uv sync
```

## Architecture

```
main.py              # FastAPI app initialization, lifespan, router registration
├── routers/         # API route handlers (thin layer, delegates to services)
│   └── auth_router.py
├── service/         # Business logic layer (single responsibility, reusable)
│   └── auth_service.py
├── auth/            # Authentication utilities (cross-cutting concerns)
│   ├── security.py     # Password hashing, JWT creation/verification
│   └── dependency.py   # FastAPI dependencies (get_user for protected routes)
├── models/          # SQLModel ORM table definitions
│   └── user.py
├── schema/          # Pydantic request/response schemas (validation layer)
│   └── user.py
├── db/              # Database configuration
│   ├── engine.py       # SQLAlchemy engine creation
│   └── session.py      # Session management, table creation
└── config/          # Application configuration
    └── settings.py     # Pydantic settings with .env loading
```

## Architectural Principles

### Layered Architecture
- **Routers** handle HTTP concerns only (request parsing, response formatting, status codes)
- **Services** contain business logic and should be reusable (no FastAPI dependencies)
- **Models** define database tables (SQLModel combines SQLAlchemy + Pydantic)
- **Schemas** define API contracts (input validation, output serialization)

### Dependency Injection
- Use FastAPI's `Depends()` for database sessions and authentication
- `get_session` yields SQLModel Session for each request
- `get_user` extracts and validates JWT from cookies, returns authenticated user

### Configuration
- Settings loaded via Pydantic's `BaseSettings` from `.env` file
- Use `@lru_cache` for singleton pattern (settings instance created once)

### Authentication Flow
1. Register: hash password → store user
2. Login: verify password → generate access_token (1d) + refresh_token (7d) → set HTTP-only cookies
3. Protected routes: `Depends(get_user)` validates JWT and injects user
4. Refresh: use refresh_token to issue new access_token

## Code Style Guidelines

### Single Responsibility
- Each module should have one reason to change
- Services should not know about HTTP (no Request, Response, HTTPException)
- Return domain objects from services; let routers handle HTTP responses

### Dependency Injection Over Imports
- Use FastAPI's dependency injection for testability
- Services can receive dependencies in `__init__` for easier mocking

### Error Handling
- Raise `HTTPException` in routers, not services
- Services should return results or raise domain exceptions

### Database Sessions
- Always use `yield` pattern for session injection
- Sessions are automatically closed after request

### Security
- Always use HTTP-only cookies for tokens (prevents XSS)
- Never log or expose JWT tokens or passwords
- Use Argon2 for password hashing (memory-hard, resistant to GPU attacks)