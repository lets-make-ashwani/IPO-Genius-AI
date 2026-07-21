'use client';

import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { useState } from 'react';
import { ChevronDown, Search } from 'lucide-react';

export default function FAQ() {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState<'All' | 'General' | 'AI Features' | 'Pricing' | 'Account'>('All');
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  const categories = ['All', 'General', 'AI Features', 'Pricing', 'Account'];

  const faqItems = [
    { category: 'General', q: 'What is IPO Genius AI?', a: 'IPO Genius AI is an advanced analysis platform that reviews draft red herring prospectuses (DRHP), financial sheets, and market sentiment to deliver accurate IPO scores, risks, and recommendations.' },
    { category: 'General', q: 'Is the AI analysis reliable?', a: 'Yes. Our AI engine uses machine learning and natural language processing models trained on historical financial data and IPO performances. However, it should only be used as a research assistant, not direct financial advice.' },
    { category: 'AI Features', q: 'What is the AI Score?', a: 'The AI Score (0-100) measures an IPO\'s relative valuation, operational health, market context, and historical promoter performances, with higher scores indicating higher listing day gain probability.' },
    { category: 'AI Features', q: 'How does the SWOT analysis work?', a: 'Our AI scans structural DRHP clauses to automatically categorize operational strengths, margin weaknesses, growth opportunities, and regulatory litigations (threats).' },
    { category: 'Pricing', q: 'What is included in the Free plan?', a: 'The Free plan offers access to the IPO calendar, basic listing profiles, and 3 AI-generated analyses per month, along with standard email notifications.' },
    { category: 'Pricing', q: 'Can I cancel my subscription anytime?', a: 'Absolutely. There are no lock-in contracts. You can downgrade or cancel your Pro Plan subscription at any time with one click from the billing tab.' },
    { category: 'Account', q: 'How do I set up alerts?', a: 'Once registered, you can activate real-time email and Telegram notification triggers directly inside your dashboard settings panel.' },
    { category: 'Account', q: 'Is my personal data secure?', a: 'Yes. We utilize industry-standard TLS encryption protocols and secure databases to store passwords and profile credentials. We never sell your personal data.' }
  ];

  const jsonLdFaq = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqItems.map(item => ({
      '@type': 'Question',
      name: item.q,
      acceptedAnswer: {
        '@type': 'Answer',
        text: item.a
      }
    }))
  };

  const filteredFaqs = faqItems.filter((item) => {
    const matchesSearch = item.q.toLowerCase().includes(searchQuery.toLowerCase()) || item.a.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = activeCategory === 'All' || item.category === activeCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="min-h-screen bg-dark-bg text-text-primary flex flex-col pt-16">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdFaq) }}
      />
      <Navbar />

      <main className="flex-1 py-16 px-4 sm:px-6 text-center max-w-4xl mx-auto w-full">
        <span className="text-xs font-bold text-primary-blue bg-primary-blue/10 px-3.5 py-1.5 rounded-full uppercase tracking-wider mb-4 inline-block">
          Support Center
        </span>
        <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white mb-8">
          Frequently Asked Questions
        </h1>

        {/* Search */}
        <div className="relative max-w-lg mx-auto mb-10">
          <Search className="absolute left-3.5 top-3 w-5 h-5 text-text-muted" />
          <input
            type="text"
            placeholder="Search FAQs..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full h-11 pl-11 pr-4 rounded-lg bg-card-bg border border-border-subtle focus:border-primary-blue text-sm focus:outline-none text-white placeholder:text-text-muted transition-all"
          />
        </div>

        {/* Filter Categories */}
        <div className="flex flex-wrap justify-center gap-2 mb-12">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat as any)}
              className={`px-4 py-2 rounded-full text-xs font-semibold transition-all min-h-[44px] ${
                activeCategory === cat
                  ? 'bg-primary-blue text-white shadow-lg shadow-primary-blue/20'
                  : 'bg-card-bg text-text-secondary hover:text-white border border-border-subtle'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* FAQ List */}
        <div className="space-y-4 text-left">
          {filteredFaqs.length > 0 ? (
            filteredFaqs.map((item, idx) => {
              const isOpen = openFaq === idx;
              return (
                <div
                  key={idx}
                  className="bg-card-bg border border-border-strong rounded-lg overflow-hidden transition-colors"
                >
                  <button
                    onClick={() => setOpenFaq(isOpen ? null : idx)}
                    className="w-full p-5 text-left flex justify-between items-center gap-4 text-white font-semibold text-sm sm:text-base hover:text-primary-blue transition-colors min-h-[44px]"
                  >
                    <span>{item.q}</span>
                    <ChevronDown className={`w-5 h-5 shrink-0 transition-transform ${isOpen ? 'rotate-180 text-primary-blue' : 'text-text-muted'}`} />
                  </button>
                  {isOpen && (
                    <div className="px-5 pb-5 pt-0 text-xs sm:text-sm text-text-secondary border-t border-border-subtle/40 leading-relaxed">
                      {item.a}
                    </div>
                  )}
                </div>
              );
            })
          ) : (
            <div className="p-8 text-center text-text-muted bg-card-bg border border-border-strong rounded-lg">
              No questions found matching your search term.
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}
