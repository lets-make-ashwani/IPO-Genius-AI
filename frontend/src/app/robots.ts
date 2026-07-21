import { MetadataRoute } from 'next';

const siteUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://ipogeniusai.vercel.app';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: [
          '/admin',
          '/admin/*',
          '/api/internal',
          '/dashboard/profile',
          '/dashboard/settings',
        ],
      },
    ],
    sitemap: `${siteUrl}/sitemap.xml`,
  };
}
