# System Architecture

# Project

IPO Genius AI

---

# High Level Architecture

                User
                  │
                  │
        Next.js Frontend
                  │
                  │
         FastAPI Backend
                  │
     ┌────────────┼────────────┐
     │            │            │
 PostgreSQL    OpenAI API     n8n
     │            │            │
     └────────────┼────────────┘
                  │
            Deployment

---

# Frontend

Technology

- Next.js
- React
- TypeScript
- Tailwind CSS
- Shadcn UI

Responsibilities

- UI
- Authentication
- Dashboard
- API Calls
- State Management
- Forms

---

# Backend

Technology

- FastAPI

Responsibilities

- Authentication
- Business Logic
- CRUD APIs
- AI Integration
- Payment Integration
- Notifications

---

# Database

Technology

- PostgreSQL

Stores

- Users
- IPOs
- AI Analysis
- Watchlist
- Notifications
- Payments

---

# AI

Technology

- OpenAI

Responsibilities

- IPO Summary
- SWOT
- Financial Analysis
- Risk Analysis
- AI Chat
- IPO Score

---

# Automation

Technology

- n8n

Responsibilities

- Collect IPO Data
- Download DRHP
- AI Trigger
- Notifications
- Scheduled Jobs

---

# Deployment

Frontend

Vercel

Backend

Render

Database

Neon PostgreSQL

Automation

n8n

---

# Authentication Flow

User

↓

Login

↓

Backend

↓

JWT

↓

Dashboard

---

# IPO Flow

Admin

↓

Add IPO

↓

Database

↓

Dashboard

↓

User

---

# AI Flow

User

↓

Open IPO

↓

Backend

↓

OpenAI

↓

AI Response

↓

Frontend

---

# Notification Flow

n8n

↓

Backend

↓

Email

Telegram

Dashboard

↓

User

---

# Folder Structure

Frontend

↓

Components

↓

Features

↓

Pages

Backend

↓

Modules

↓

Services

↓

Database

↓

API

---

# Architecture Rules

- Keep frontend and backend independent.
- Backend owns all business logic.
- Frontend never directly accesses the database.
- AI is always called through the backend.
- n8n never contains business logic.
- APIs should remain modular.

---

# Development Flow

ChatGPT

↓

Documentation

↓

Antigravity

↓

Code Generation

↓

Testing

↓

Deployment

---

# Goal

Build a scalable, modular, and production-ready architecture that can grow without major redesign.