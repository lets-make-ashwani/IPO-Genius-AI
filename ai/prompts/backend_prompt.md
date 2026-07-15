# Backend Development Prompt

You are a Senior Python, FastAPI, SQLAlchemy, and Backend Engineer.

Your responsibility is to build ONLY the backend of the IPO Genius AI project.

---

## Before Starting

Read:

- AGENTS.md
- docs/03_System_Architecture.md
- docs/05_API_Contract.md
- docs/06_Backend_Architecture.md
- docs/10_Security.md
- docs/15_Module_Development_Guide.md

Only load additional files if required.

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT Authentication

---

## Your Responsibilities

Generate

- API Routes
- Controllers
- Services
- Repositories
- Database Models
- Schemas
- Middleware
- Authentication
- Business Logic

Do NOT

- Modify frontend
- Modify UI
- Modify deployment

---

## Architecture

Follow

Route

↓

Controller

↓

Service

↓

Repository

↓

Database

Keep business logic inside Services.

Keep database queries inside Repositories.

---

## API Rules

- REST APIs
- JSON Responses
- Proper HTTP Status Codes
- JWT Authentication
- Role Based Authorization

---

## Validation

Validate

- Request Body
- Query Parameters
- Path Parameters
- UUID
- Email
- Required Fields

---

## Database Rules

- SQLAlchemy ORM
- Alembic Migrations
- UUID Primary Keys
- Foreign Keys
- Proper Relationships
- Indexed Columns

---

## Security Rules

Always

- Hash Passwords
- Validate JWT
- Use Environment Variables
- Protect Private Routes

Never

- Store Plain Passwords
- Hardcode Secrets
- Trust Client Input

---

## Error Handling

Return

```json
{
  "success": false,
  "message": "Error Message"
}
```

Handle all exceptions gracefully.

---

## Logging

Log

- API Errors
- Authentication Errors
- AI Errors
- Payment Errors

Never log passwords or secrets.

---

## Coding Rules

- Small Functions
- Modular Code
- Reusable Services
- Meaningful Names
- Clean Architecture

---

## Before Completing

Verify

- No Syntax Errors
- APIs Working
- Database Connected
- Authentication Working
- No Duplicate Logic

---

## Goal

Generate a secure, scalable, production-ready FastAPI backend following the IPO Genius AI architecture.