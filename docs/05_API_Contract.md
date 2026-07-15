# API Contract

# Base URL

/api/v1

---

# Response Format

Success

```json
{
  "success": true,
  "message": "Request successful",
  "data": {}
}
```

Error

```json
{
  "success": false,
  "message": "Something went wrong",
  "errors": []
}
```

---

# Authentication

## Register

POST

/auth/register

---

## Login

POST

/auth/login

---

## Logout

POST

/auth/logout

---

## Forgot Password

POST

/auth/forgot-password

---

## Reset Password

POST

/auth/reset-password

---

## Get Profile

GET

/users/me

---

## Update Profile

PUT

/users/me

---

# IPO APIs

## Get All IPOs

GET

/ipos

---

## Upcoming IPOs

GET

/ipos/upcoming

---

## Open IPOs

GET

/ipos/open

---

## Closed IPOs

GET

/ipos/closed

---

## Listed IPOs

GET

/ipos/listed

---

## IPO Details

GET

/ipos/{id}

---

## Search IPO

GET

/ipos/search

---

# AI APIs

## AI Summary

GET

/ai/summary/{ipoId}

---

## AI Score

GET

/ai/score/{ipoId}

---

## SWOT Analysis

GET

/ai/swot/{ipoId}

---

## Risk Analysis

GET

/ai/risk/{ipoId}

---

## AI Chat

POST

/ai/chat

---

# Watchlist APIs

## Get Watchlist

GET

/watchlist

---

## Add IPO

POST

/watchlist

---

## Remove IPO

DELETE

/watchlist/{id}

---

# Notification APIs

## Get Notifications

GET

/notifications

---

## Mark as Read

PUT

/notifications/{id}

---

# Subscription APIs

## Plans

GET

/subscriptions/plans

---

## Current Plan

GET

/subscriptions/me

---

## Upgrade

POST

/subscriptions/upgrade

---

# Payment APIs

## Create Order

POST

/payments/create-order

---

## Verify Payment

POST

/payments/verify

---

## Payment History

GET

/payments/history

---

# Admin APIs

## Dashboard

GET

/admin/dashboard

---

## Users

GET

/admin/users

---

## IPOs

GET

/admin/ipos

---

## Create IPO

POST

/admin/ipos

---

## Update IPO

PUT

/admin/ipos/{id}

---

## Delete IPO

DELETE

/admin/ipos/{id}

---

## Run AI Analysis

POST

/admin/ai/run/{ipoId}

---

# HTTP Status Codes

200 OK

201 Created

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

500 Internal Server Error

---

# API Rules

- Use REST APIs
- Validate all requests
- Return JSON only
- Keep responses consistent
- Protect private routes using JWT
- Use pagination for list endpoints
- Never expose sensitive information

---

# Goal

Provide a clean, consistent, and scalable API structure for frontend and backend communication.