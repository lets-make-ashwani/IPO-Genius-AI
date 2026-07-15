# Automation Workflow

# Platform

- n8n

---

# Purpose

Use n8n only for automation.

Never place business logic inside n8n.

Business logic always belongs in the FastAPI backend.

---

# Automation List

- IPO Data Collection
- DRHP Download
- AI Analysis Trigger
- Notifications
- Scheduled Tasks

---

# Workflow 1

## IPO Data Collection

Schedule

↓

Check IPO Sources

↓

New IPO Found?

↓

Yes

↓

Backend API

↓

Save Database

↓

Notify Admin

---

# Workflow 2

## DRHP Collection

New IPO

↓

Download DRHP

↓

Upload File

↓

Store URL

↓

Notify Backend

---

# Workflow 3

## AI Analysis

New IPO

↓

Backend API

↓

OpenAI

↓

Save AI Analysis

↓

Complete

---

# Workflow 4

## Notifications

Trigger

↓

Backend

↓

Email

↓

Telegram

↓

Dashboard Notification

---

# Workflow 5

## Daily Scheduler

Run Every Day

↓

Check IPO Status

↓

Update Status

↓

Send Notifications

---

# Workflow 6

## Subscription Reminder

Subscription Ending

↓

Notify User

↓

Email

↓

Dashboard

---

# External Sources

Examples

- NSE
- BSE
- SEBI
- Company Websites

Backend validates all incoming data before saving.

---

# Backend Integration

n8n

↓

FastAPI API

↓

Database

Never connect n8n directly to the database.

---

# Error Handling

If workflow fails

- Retry
- Log Error
- Notify Admin

Never stop other workflows.

---

# Logging

Log

- Workflow Start
- Workflow End
- Success
- Failure

---

# Security

- Secure Webhooks
- API Authentication
- Environment Variables
- Never expose secrets

---

# Rules

- No business logic
- No direct database access
- Always use backend APIs
- Validate all incoming data
- Keep workflows modular

---

# Goal

Automate repetitive tasks while keeping the application secure, scalable, and easy to maintain.