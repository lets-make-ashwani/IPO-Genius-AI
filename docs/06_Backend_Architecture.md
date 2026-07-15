# Backend Architecture

# Framework

- FastAPI
- Python
- SQLAlchemy
- Alembic
- PostgreSQL

---

# Architecture

Client

↓

API Routes

↓

Controllers

↓

Services

↓

Repositories

↓

Database

---

# Folder Structure

backend/

app/

config/

modules/

shared/

database/

tests/

---

# Modules

authentication/

users/

ipos/

ai/

watchlist/

notifications/

payments/

subscriptions/

admin/

settings/

analytics/

---

# Every Module Structure

module/

controllers/

services/

repositories/

schemas/

models/

routes/

utils/

---

# Responsibilities

## Routes

- API Endpoints
- Request Mapping

---

## Controllers

- Handle Request
- Return Response

---

## Services

- Business Logic
- Validation
- AI Calls
- Calculations

---

## Repository

- Database Queries
- CRUD Operations

---

## Models

- SQLAlchemy Models

---

## Schemas

- Request Validation
- Response Validation

---

# Authentication

JWT Authentication

Protected Routes

Role Based Access

Roles

- Guest
- User
- Premium
- Admin

---

# Database

PostgreSQL

ORM

SQLAlchemy

Migration

Alembic

---

# AI Integration

Backend

↓

OpenAI

↓

AI Response

↓

Database

↓

Frontend

---

# Notification Flow

Backend

↓

Email

Telegram

Database

↓

User

---

# Payment Flow

Frontend

↓

Backend

↓

Razorpay

↓

Verification

↓

Database

↓

User

---

# Error Handling

Always return

```json
{
  "success": false,
  "message": "Error Message"
}
```

Never expose internal errors.

---

# Logging

Log

- API Errors
- AI Errors
- Payment Errors
- Authentication Errors

---

# Validation

Validate

- Email
- Password
- UUID
- Dates
- Required Fields

---

# Security

- JWT
- Password Hashing
- Environment Variables
- Rate Limiting
- Input Validation

---

# Coding Rules

- Small Functions
- Modular Code
- No Duplicate Logic
- Reusable Services
- Proper Naming

---

# Goal

Create a scalable, secure, and maintainable backend that can support future features without major changes.