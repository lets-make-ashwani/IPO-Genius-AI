# IPO Genius AI — Enterprise SEO, AIEO, GEO & LLMO Audit Matrix

* **Platform Version:** `1.0.1` (Phase 5.3)
* **Target Audience:** Technical SEO Architects, AI Search Engineers, System Operations
* **Audit Date:** 2026-07-21

---

## 1. Route-by-Route Metadata & Audit Matrix

| Route | Title & Metadata Status | Canonical URL | Open Graph & Twitter Cards | JSON-LD Schemas | Robots Directives | Verification Status |
|---|---|---|---|---|---|---|
| `/` | `VERIFIED` (Default Site Title) | `https://ipogeniusai.vercel.app/` | `website`, `summary_large_image` | `Organization`, `WebSite` | `index, follow` | `VERIFIED` |
| `/about` | `VERIFIED` | `https://ipogeniusai.vercel.app/about` | `website`, `summary_large_image` | `Organization` | `index, follow` | `VERIFIED` |
| `/features` | `VERIFIED` | `https://ipogeniusai.vercel.app/features` | `website`, `summary_large_image` | `WebPage` | `index, follow` | `VERIFIED` |
| `/pricing` | `VERIFIED` | `https://ipogeniusai.vercel.app/pricing` | `website`, `summary_large_image` | `OfferCatalog` | `index, follow` | `VERIFIED` |
| `/faq` | `VERIFIED` | `https://ipogeniusai.vercel.app/faq` | `website`, `summary_large_image` | `FAQPage` | `index, follow` | `VERIFIED` |
| `/contact` | `VERIFIED` | `https://ipogeniusai.vercel.app/contact` | `website`, `summary_large_image` | `ContactPage` | `index, follow` | `VERIFIED` |
| `/privacy-terms` | `VERIFIED` | `https://ipogeniusai.vercel.app/privacy-terms` | `website`, `summary_large_image` | `WebPage` | `index, follow` | `VERIFIED` |
| `/login` | `VERIFIED` | `https://ipogeniusai.vercel.app/login` | `website`, `summary_large_image` | `WebPage` | `index, follow` | `VERIFIED` |
| `/register` | `VERIFIED` | `https://ipogeniusai.vercel.app/register` | `website`, `summary_large_image` | `WebPage` | `index, follow` | `VERIFIED` |
| `/dashboard` | `VERIFIED` | `https://ipogeniusai.vercel.app/dashboard` | `website`, `summary_large_image` | `BreadcrumbList` | `index, follow` | `VERIFIED` |
| `/dashboard/ipo` | `VERIFIED` | `https://ipogeniusai.vercel.app/dashboard/ipo` | `website`, `summary_large_image` | `CollectionPage` | `index, follow` | `VERIFIED` |
| `/dashboard/ipo/[id]` | `VERIFIED` (Dynamic) | `https://ipogeniusai.vercel.app/dashboard/ipo/[id]` | `website`, `summary_large_image` | `FinancialProduct`, `BreadcrumbList` | `index, follow` | `VERIFIED` |
| `/dashboard/ipo/[id]/analysis` | `VERIFIED` (Dynamic) | `https://ipogeniusai.vercel.app/dashboard/ipo/[id]/analysis` | `article`, `summary_large_image` | `Article`, `BreadcrumbList` | `index, follow` | `VERIFIED` |
| `/admin` | `VERIFIED` | `https://ipogeniusai.vercel.app/admin` | `website`, `summary_large_image` | None | `noindex, nofollow` | `VERIFIED` |

---

## 2. AI Engine Optimization (AIEO), GEO & LLMO Findings

* **GEO Recommended For / Avoid Blocks:** Implemented explicit investor target audience blocks (`Recommended For` / `Who Should Avoid`) on IPO detail pages for high-probability citations by Perplexity, ChatGPT, Claude, and Gemini.
* **Content Freshness Telemetry:** Exposed `Updated` timestamps and real-time IST time indicators on AI Analysis pages.
* **LLMO Semantic HTML:** Enforced single `<h1>` per route with structured `<article>`, `<section>`, `<header>`, and `<nav>` wrappers.

---

## 3. Verification & Compliance Checklist

* **Next.js Production Build (`npm run build`):** **31 / 31 static & dynamic routes compiled cleanly** including `sitemap.xml` and `robots.txt`.
* **Sitemap Generation:** `/sitemap.xml` dynamic revalidation configured (`1h`).
* **Robots Directives:** `/robots.txt` disallows `/admin`, `/admin/*`, `/api/internal`, `/dashboard/profile`, `/dashboard/settings`.