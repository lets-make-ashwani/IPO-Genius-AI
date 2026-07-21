# IPO Genius AI — SEO & Indexing Architecture Specification

* **Platform Version:** `1.0.1` (Phase 5.3)
* **Domain:** `https://ipogeniusai.vercel.app`

---

## 1. Metadata API Architecture

IPO Genius AI utilizes the Next.js 15 App Router Metadata API.

### Root Defaults (`app/layout.tsx`)
```ts
export const metadata: Metadata = {
  metadataBase: new URL('https://ipogeniusai.vercel.app'),
  title: {
    default: 'IPO Genius AI — AI-Powered Indian IPO Intelligence & GMP Tracker',
    template: '%s | IPO Genius AI'
  },
  description: 'Real-time Indian IPO tracking, Grey Market Premium (GMP) updates, SEBI prospectus filings, AI-driven evaluation scores...',
  // ...
};
```

---

## 2. Dynamic Sitemap & Robots Strategy

* **`/sitemap.xml`:** Generated dynamically via `app/sitemap.ts`. It queries the FastAPI backend (`GET /api/v1/ipos?limit=100`) and outputs static marketing pages plus dynamic IPO deal routes (`/dashboard/ipo/[id]`, `/dashboard/ipo/[id]/analysis`). Revalidated every 3600 seconds.
* **`/robots.txt`:** Generated via `app/robots.ts`. Allows all search crawlers on public routes while disallowing private admin routes (`Disallow: /admin`, `Disallow: /api/internal`).

---

## 3. Structured Data Architecture (JSON-LD)

1. **Organization & WebSite Schema:** Embedded in root `layout.tsx` for brand authority and site search action.
2. **FAQPage Schema:** Embedded in `app/faq/page.tsx` for rich Google search snippets.
3. **FinancialProduct & Article Schema:** Embedded dynamically in `app/dashboard/ipo/[id]/page.tsx` and `analysis/page.tsx`.
