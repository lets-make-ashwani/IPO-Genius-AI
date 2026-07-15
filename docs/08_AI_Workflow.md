# AI Workflow

# AI Provider

- OpenAI API

The AI provider should be configurable so it can be changed in the future.

---

# AI Features

- IPO Summary
- SWOT Analysis
- Risk Analysis
- Financial Analysis
- IPO Score
- AI Chat

---

# AI Workflow

User

↓

Select IPO

↓

Frontend

↓

Backend

↓

OpenAI API

↓

AI Response

↓

Database (Optional Cache)

↓

Frontend

↓

User

---

# AI Summary

Generate

- Company Overview
- Business Model
- Key Highlights
- Investment Summary

---

# SWOT Analysis

Generate

- Strengths
- Weaknesses
- Opportunities
- Threats

---

# Risk Analysis

Generate

- Business Risks
- Financial Risks
- Market Risks
- Industry Risks

---

# Financial Analysis

Analyze

- Revenue
- Profit
- Growth
- Debt
- Valuation

---

# IPO Score

Generate score out of 100.

Example

Financial Health

30%

Business Quality

25%

Growth

20%

Risk

15%

Valuation

10%

↓

Final AI Score

---

# AI Chat

Users can ask questions like

- Should I invest?
- Explain this IPO.
- What are the risks?
- Compare with another IPO.
- Explain financial terms.

---

# AI Input

AI receives

- IPO Details
- Financial Data
- DRHP Data
- User Question (if any)

---

# AI Output

Return

- Summary
- Explanation
- Recommendation
- Confidence Level

---

# AI Rules

- Never generate fake financial data.
- Never guarantee profits.
- Explain every recommendation.
- Keep responses easy to understand.
- Mention uncertainty when required.

---

# Prompt Rules

Always provide AI with

- Company Information
- Financial Information
- IPO Details
- User Question

Never send empty or incomplete data.

---

# Caching

Cache AI responses when possible.

Generate again only if

- IPO data changes
- Admin requests regeneration

---

# Error Handling

If AI fails

- Return a friendly error message.
- Never crash the application.
- Allow retry.

---

# Goal

Provide simple, accurate, and understandable AI-powered IPO analysis for every user.