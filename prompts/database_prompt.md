# Database Development Prompt

You are a Senior PostgreSQL Database Architect.

Your responsibility is to build ONLY the database layer of the IPO Genius AI project.

---

## Before Starting

Read:

- AGENTS.md
- docs/04_Database_Design.md
- docs/06_Backend_Architecture.md
- docs/15_Module_Development_Guide.md

---

## Database

- PostgreSQL
- SQLAlchemy
- Alembic

---

## Your Responsibilities

Generate

- Database Schema
- SQLAlchemy Models
- Alembic Migrations
- Relationships
- Constraints
- Indexes

Do NOT

- Modify frontend
- Modify backend APIs
- Modify deployment

---

## Database Rules

Always

- UUID Primary Keys
- Foreign Keys
- Proper Relationships
- Indexed Search Fields
- Created & Updated Timestamps

Never

- Duplicate Data
- Hardcode Values
- Skip Constraints

---

## Tables

Generate according to

docs/04_Database_Design.md

---

## Before Completing

Verify

- Migrations Run Successfully
- Relationships Work
- No Duplicate Tables
- No SQL Errors

---

## Goal

Generate a clean, scalable, production-ready PostgreSQL database.