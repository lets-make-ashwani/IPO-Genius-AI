# IPO Genius AI — Structured Data (JSON-LD) Reference Guide

* **Version:** `1.0.1` (Phase 5.3)

---

## 1. Supported Schema Types

| Schema Type | Context / Route | Purpose |
|---|---|---|
| `Organization` | `RootLayout` (`app/layout.tsx`) | Establishes brand entity identity & logo for Google Knowledge Graph. |
| `WebSite` | `RootLayout` (`app/layout.tsx`) | Enables Sitelinks Search Box in Google search results. |
| `FAQPage` | `/faq` (`app/faq/page.tsx`) | Enables Rich FAQ accordion snippets in search result pages. |
| `FinancialProduct` | `/dashboard/ipo/[id]` | Structured financial deal metrics (price, lot size, currency). |
| `Article` | `/dashboard/ipo/[id]/analysis` | News & analysis article metadata for Google Discover & News. |
| `BreadcrumbList` | Dashboard sub-routes | Rich breadcrumb trail in search result listings. |

---

## 2. Validation & Testing

Validate JSON-LD outputs using:
* [Google Rich Results Test](https://search.google.com/test/rich-results)
* [Schema.org Validator](https://validator.schema.org)
