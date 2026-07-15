# Project Constitution

## Project Name

IPO Genius AI

---

# Purpose

Build a production-ready AI-powered IPO research platform that is fast, scalable, responsive, and easy to maintain.

The project should always prioritize:

- Simplicity
- Reusability
- Performance
- Clean Architecture
- Great User Experience

---

# Core Principles

1. Keep the code simple.
2. Build reusable components.
3. Avoid duplicate code.
4. Prefer readability over cleverness.
5. Every module should be independent.
6. Mobile First Design.
7. Performance matters.
8. Security is mandatory.
9. AI should assist users, not replace financial decisions.
10. Documentation should stay synchronized with the code.

---

# Tech Stack

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- Shadcn UI

## Backend

- FastAPI
- SQLAlchemy
- Alembic

## Database

- PostgreSQL

## AI

- OpenAI API

## Automation

- n8n

## Deployment

- Vercel
- Render
- Neon PostgreSQL

---

# UI Principles

The interface should be:

- Clean
- Professional
- Modern
- Responsive
- Accessible
- Fast

Use a consistent design system across the application.

---

# Coding Principles

Always:

- Write modular code.
- Create reusable components.
- Keep functions small.
- Use meaningful names.
- Handle errors properly.
- Remove unused code.

Never:

- Hardcode sensitive data.
- Duplicate logic.
- Create unnecessary complexity.
- Ignore TypeScript errors.
- Leave debugging code in production.

---

# Folder Structure

Follow the official project folder structure.

Never change the architecture without updating the documentation.

---

# API Rules

Every API should:

- Validate input
- Return consistent responses
- Handle errors properly
- Be documented

Standard Response

```json
{
  "success": true,
  "message": "",
  "data": {}
}
```

---

# Database Rules

- UUID Primary Keys
- Proper Relationships
- Indexed Search Fields
- Soft Delete when required
- Never store duplicate data

---

# AI Rules

AI should:

- Explain its analysis
- Never invent financial information
- Show confidence where appropriate
- Keep responses simple

---

# Automation Rules

n8n is responsible for:

- Scheduled Jobs
- IPO Collection
- Notifications
- Background Tasks

Business logic always belongs in the backend.

---

# Security Rules

- Authentication required where needed
- Validate every request
- Use environment variables
- Never expose secrets
- Protect private APIs

---

# Definition of Done

A feature is complete when:

- It works correctly
- It is responsive
- It has no build errors
- It has no lint errors
- It follows the project architecture
- It is documented if necessary

---

# Development Philosophy

Build a working product first.

Improve and optimize after the application is functional.

Avoid over-engineering.

Focus on delivering value.