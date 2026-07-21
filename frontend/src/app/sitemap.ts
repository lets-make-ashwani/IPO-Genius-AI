import { MetadataRoute } from 'next';

const siteUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://ipogeniusai.vercel.app';
const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  // Static marketing & public pages
  const staticRoutes: MetadataRoute.Sitemap = [
    {
      url: `${siteUrl}/`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1.0,
    },
    {
      url: `${siteUrl}/about`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${siteUrl}/features`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${siteUrl}/pricing`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.9,
    },
    {
      url: `${siteUrl}/faq`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    {
      url: `${siteUrl}/contact`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.6,
    },
    {
      url: `${siteUrl}/privacy-terms`,
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 0.5,
    },
    {
      url: `${siteUrl}/dashboard/ipo`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.9,
    },
    // Dynamic Date-driven public category routes
    {
      url: `${siteUrl}/ipos/live`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.95,
    },
    {
      url: `${siteUrl}/ipos/upcoming`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.95,
    },
    {
      url: `${siteUrl}/ipos/recently-listed`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.9,
    },
    {
      url: `${siteUrl}/ipos/recently-closed`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.9,
    },
    {
      url: `${siteUrl}/ipos/top-rated`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.9,
    },
    {
      url: `${siteUrl}/ipos/highest-gmp`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.9,
    },
    {
      url: `${siteUrl}/ipos/most-subscribed`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.9,
    },
    {
      url: `${siteUrl}/ipos/trending`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.9,
    },
  ];

  // Dynamic IPO detail and analysis routes fetched from API
  let ipoRoutes: MetadataRoute.Sitemap = [];
  try {
    const res = await fetch(`${backendUrl}/api/v1/ipos?limit=100`, {
      next: { revalidate: 3600 }
    });
    if (res.ok) {
      const body = await res.json();
      const ipos = body.data || [];
      ipoRoutes = ipos.flatMap((ipo: any) => [
        {
          url: `${siteUrl}/dashboard/ipo/${ipo.id}`,
          lastModified: new Date(ipo.updated_at || Date.now()),
          changeFrequency: 'daily' as const,
          priority: 0.9,
        },
        {
          url: `${siteUrl}/dashboard/ipo/${ipo.id}/analysis`,
          lastModified: new Date(ipo.updated_at || Date.now()),
          changeFrequency: 'daily' as const,
          priority: 0.85,
        },
      ]);
    }
  } catch (err) {
    console.error('Sitemap dynamic IPO fetch error:', err);
  }

  return [...staticRoutes, ...ipoRoutes];
}
