# AGENTS.md

# IPO Genius AI

## Project Overview

IPO Genius AI is an AI-powered SaaS platform that helps users analyze upcoming IPOs using AI. The application should be modern, scalable, responsive, production-ready, and easy to maintain.

This repository is the single source of truth for the project.

---

# Tech Stack

## Frontend

- Next.js (App Router)
- React
- TypeScript
- Tailwind CSS
- Shadcn UI
- React Hook Form
- Zod
- TanStack Query

## Backend

- FastAPI
- Python
- SQLAlchemy
- Alembic

## Database

- PostgreSQL

## AI

- OpenAI API

## Automation

- n8n

## Deployment

- Frontend → Vercel
- Backend → Render
- Database → Neon PostgreSQL

---

# Repository Rules

- Never change the folder structure.
- Never rename APIs without updating documentation.
- Never rename database tables without updating migrations.
- Never duplicate components.
- Always reuse existing code.
- Keep the project modular.
- Write clean and maintainable code.

---

# Before Starting Any Task

1. Understand the requested task.
2. Read AGENTS.md.
3. Load only the required documentation.
4. Create a plan.
5. Generate production-ready code.
6. Verify the solution before finishing.

---

# Context Loading Rules

Always read:

- AGENTS.md

Read only if required:

- docs/
- prompts/
- skills/

Do not load unrelated files.

---

# Coding Standards

## Frontend

- TypeScript only
- Functional Components
- Mobile First
- Responsive Design
- Reusable Components
- Use Tailwind CSS
- Use Shadcn UI components whenever possible

## Backend

- REST API
- Async functions
- Proper validation
- Layered Architecture
- Small reusable services

## Database

- PostgreSQL
- UUID Primary Keys
- Proper Relationships
- Index important columns
- Never hardcode data

---

# UI Rules

- Modern SaaS UI
- Professional appearance
- Clean spacing
- Consistent colors
- Accessible
- Responsive
- Light & Dark mode support

---

# API Rules

- RESTful APIs
- Standard HTTP Status Codes
- Consistent JSON responses

Example

{
  "success": true,
  "message": "",
  "data": {}
}

---

# AI Rules

- AI should explain every recommendation.
- Never fabricate financial information.
- Clearly indicate when information is unavailable.
- Responses should be concise and understandable.

---

# Automation Rules

n8n is responsible only for:

- Scheduled Jobs
- IPO Collection
- Notifications
- AI Triggers

Business logic always remains inside the backend.

---

# Security Rules

- Validate all inputs.
- Never expose secrets.
- Use environment variables.
- Protect private APIs.
- Implement authentication and authorization.

---

# Testing Rules

Every feature must:

- Build successfully
- Pass lint checks
- Be responsive
- Handle errors gracefully

---

# Definition of Done

A task is complete only if:

- Feature works correctly.
- Code is clean.
- No duplicate logic.
- Responsive on all devices.
- No console errors.
- No TypeScript errors.
- No lint errors.

---

# If Something Is Unclear

Do not guess.

Analyze the existing project.

Reuse existing architecture.

Follow existing patterns.

If a decision could affect multiple modules, request clarification instead of making assumptions.

---

# Goal

Build a production-ready IPO Genius AI platform with clean architecture, reusable components, scalable code, and consistent design.

Always prioritize quality, maintainability, and simplicity.


## MCP Rules

If the task is related to UI, UX, Figma, wireframes, mockups, design systems, components, layouts, or visual design:

Always use the connected Google Stitch MCP server.

Do not generate React code until the design is approved.

After approval, convert the approved Stitch design into Next.js components.