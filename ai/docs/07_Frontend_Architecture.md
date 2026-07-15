# Frontend Architecture

# Framework

- Next.js (App Router)
- React
- TypeScript
- Tailwind CSS
- Shadcn UI

---

# Folder Structure

frontend/

app/

components/

features/

hooks/

services/

utils/

types/

constants/

styles/

public/

---

# Components

Reusable Components

- Button
- Card
- Input
- Modal
- Table
- Badge
- Avatar
- Loader
- Pagination

Layout Components

- Header
- Navbar
- Sidebar
- Footer

Feature Components

- IPO Card
- AI Card
- Watchlist Card
- Notification Card
- Dashboard Widgets

---

# Feature Modules

authentication/

dashboard/

ipo/

ai/

watchlist/

notifications/

profile/

subscription/

admin/

---

# Page Structure

Public

- Home
- Features
- Pricing
- About
- Contact
- Login
- Register

User

- Dashboard
- IPO List
- IPO Details
- AI Analysis
- Watchlist
- Notifications
- Profile
- Settings

Admin

- Dashboard
- IPO Management
- User Management
- Analytics

---

# Layouts

Public Layout

Authentication Layout

Dashboard Layout

Admin Layout

---

# State Management

Use

- React Hooks
- Context API

Use TanStack Query for

- API Requests
- Caching
- Data Fetching

---

# Forms

Use

- React Hook Form
- Zod Validation

---

# API Communication

Frontend

↓

API Service

↓

Backend

Never call APIs directly inside UI components.

---

# Styling Rules

Use

- Tailwind CSS

Use Shadcn UI components whenever possible.

Avoid custom CSS unless necessary.

---

# Responsive Design

Support

- Mobile
- Tablet
- Laptop
- Desktop

Mobile First Development.

---

# Navigation

Guest

Home

↓

Login

↓

Register

User

Dashboard

↓

IPO

↓

Details

↓

AI

↓

Watchlist

Admin

Dashboard

↓

Manage IPO

↓

Users

↓

Analytics

---

# Loading States

Every page should have

- Loading State
- Empty State
- Error State

---

# Error Handling

Show user-friendly messages.

Never expose backend errors.

---

# Performance

- Lazy Load Pages
- Lazy Load Images
- Optimize API Calls
- Reuse Components

---

# UI Rules

- Keep components reusable.
- Avoid duplicate UI.
- Keep spacing consistent.
- Use the design system.
- Follow accessibility standards.

---

# Coding Rules

- Functional Components Only
- TypeScript Only
- Small Components
- Meaningful Names
- Clean Folder Structure
- Reusable Logic

---

# Goal

Build a fast, responsive, scalable, and maintainable frontend with reusable components and a consistent user experience.