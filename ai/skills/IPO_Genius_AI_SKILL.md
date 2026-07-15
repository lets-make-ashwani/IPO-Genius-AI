# IPO Genius AI Skill

## Purpose

This skill defines how to build features inside the IPO Genius AI project.

Always follow these rules.

---

## Development Order

Understand Feature

↓

Design UI

↓

Create Frontend

↓

Create Backend

↓

Create Database

↓

Connect APIs

↓

Test

↓

Deploy

---

## Folder Rules

Never change the existing folder structure.

Never create duplicate folders.

Always place files inside the correct module.

---

## Frontend Rules

- Reuse existing components.
- Mobile First.
- TypeScript only.
- Tailwind CSS.
- Shadcn UI.
- Keep components small.
- One responsibility per component.

---

## Backend Rules

- REST APIs.
- Layered Architecture.
- Business logic inside Services.
- Database logic inside Repositories.
- JWT Authentication.

---

## Database Rules

- PostgreSQL.
- UUID IDs.
- Foreign Keys.
- Proper Relationships.
- Use Migrations.

---

## API Rules

Every API should

- Validate Input
- Return JSON
- Handle Errors
- Use Proper Status Codes

---

## AI Rules

AI should

- Explain recommendations.
- Never generate fake information.
- Return structured responses.

---

## Automation Rules

Use n8n only for

- Scheduling
- Notifications
- IPO Collection

Never put business logic inside n8n.

---

## UI Rules

Every page should

- Be Responsive
- Support Dark Mode
- Be Accessible
- Follow the Design System

---

## Before Completing Any Task

Verify

- Build Success
- No TypeScript Errors
- No Lint Errors
- Responsive UI
- API Connected
- Database Connected

---

## Goal

Build every module using the same architecture, coding standards, and project rules.