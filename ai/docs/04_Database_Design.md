# Database Design

# Database

PostgreSQL

---

# Naming Rules

- Use snake_case
- Table names should be plural
- Primary Key: id
- Foreign Key: table_name_id
- Use UUID for IDs
- Store timestamps in UTC

---

# Tables

## users

- id
- full_name
- email
- password
- avatar
- role
- is_active
- created_at
- updated_at

---

## ipos

- id
- company_name
- logo
- sector
- exchange
- price_band
- lot_size
- issue_size
- open_date
- close_date
- listing_date
- status
- drhp_url
- created_at
- updated_at

---

## ipo_details

- id
- ipo_id
- company_overview
- business_model
- strengths
- weaknesses
- promoters
- objectives
- financial_summary

---

## ai_analysis

- id
- ipo_id
- summary
- swot
- risk_analysis
- financial_analysis
- recommendation
- ai_score
- generated_at

---

## watchlists

- id
- user_id
- ipo_id
- created_at

---

## notifications

- id
- user_id
- title
- message
- type
- is_read
- created_at

---

## subscriptions

- id
- user_id
- plan
- status
- start_date
- end_date

---

## payments

- id
- user_id
- subscription_id
- payment_id
- amount
- status
- provider
- created_at

---

## settings

- id
- user_id
- theme
- language
- email_notifications
- telegram_notifications

---

# Relationships

users

↓

watchlists

↓

ipos

--------------------

users

↓

subscriptions

↓

payments

--------------------

ipos

↓

ipo_details

↓

ai_analysis

--------------------

users

↓

notifications

---

# Indexes

Create indexes for

- email
- company_name
- open_date
- listing_date
- status
- user_id
- ipo_id

---

# Data Rules

- Email must be unique.
- One AI analysis per IPO.
- One watchlist record per user and IPO.
- Never duplicate IPO records.
- Use soft delete if required.

---

# ER Diagram

users

↓

watchlists

↓

ipos

↓

ipo_details

↓

ai_analysis

↓

notifications

↓

subscriptions

↓

payments

---

# Future Tables

- news
- ipo_news
- portfolio
- portfolio_transactions
- ai_chat_history
- activity_logs
- audit_logs

---

# Goal

Keep the database normalized, scalable, and easy to maintain.