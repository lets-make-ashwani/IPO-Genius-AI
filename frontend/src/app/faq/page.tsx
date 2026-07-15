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

  const filteredFaqs = faqItems.filter((item) => {
    const matchesSearch = item.q.toLowerCase().includes(searchQuery.toLowerCase()) || item.a.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = activeCategory === 'All' || item.category === activeCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="min-h-screen bg-dark-bg text-text-primary flex flex-col pt-16">
      <Navbar />

      <section className="py-20 px-6 text-center max-w-4xl mx-auto w-full">
        <span className="text-xs font-bold text-primary-blue bg-primary-blue/10 px-3.5 py-1.5 rounded-full uppercase tracking-wider mb-4 inline-block">
          Support Center
        </span>
        <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-8">
          Frequently Asked Questions
        </h1>

        {/* Search */}
        <div className="relative max-w-lg mx-auto mb-12">
          <Search className="absolute left-3.5 top-3 w-5 h-5 text-text-muted" />
          <input
            type="text"
            placeholder="Search FAQs..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full h-12 pl-12 pr-4 rounded-md bg-card-bg/60 border border-border-subtle focus:border-primary-blue text-sm focus:outline-none focus:ring-1 focus:ring-primary-blue transition-all"
          />
        </div>

        {/* Categories */}
        <div className="flex flex-wrap items-center justify-center gap-3 mb-12">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => {
                setActiveCategory(cat as any);
                setOpenFaq(null);
              }}
              className={`text-xs font-semibold px-4 py-2 rounded-full border transition-all ${
                activeCategory === cat
                  ? 'bg-primary-blue border-primary-blue text-white'
                  : 'bg-card-bg border-border-strong text-text-secondary hover:text-white'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Accordions */}
        <div className="space-y-4 max-w-3xl mx-auto text-left mb-20">
          {filteredFaqs.length > 0 ? (
            filteredFaqs.map((faq, idx) => (
              <div key={idx} className="border border-border-strong rounded-lg overflow-hidden bg-card-bg/30">
                <button
                  onClick={() => setOpenFaq(prev => prev === idx ? null : idx)}
                  className="w-full flex items-center justify-between p-5 text-left font-semibold text-white focus:outline-none"
                >
                  <span className="pr-4">{faq.q}</span>
                  <ChevronDown className={`w-4 h-4 text-text-muted shrink-0 transition-transform ${openFaq === idx ? 'rotate-180' : ''}`} />
                </button>
                {openFaq === idx && (
                  <div className="px-5 pb-5 text-sm text-text-secondary leading-relaxed border-t border-border-strong/50 pt-3">
                    {faq.a}
                  </div>
                )}
              </div>
            ))
          ) : (
            <div className="text-center py-16 text-text-muted">
              No results found matching your search.
            </div>
          )}
        </div>
      </section>

      <Footer />
    </div>
  );
}
