'use client';

import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import Link from 'next/link';
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Calendar,
  Star,
  MessageSquare,
  Bell,
  Layers,
  ChevronDown,
  TrendingUp
} from 'lucide-react';
import { useState, useEffect } from 'react';
import { ipoService } from '../services/ipo.service';
import { IPO } from '../types';

export default function Home() {
  const [openFaq, setOpenFaq] = useState<number | null>(null);
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');
  const [featuredIPOs, setFeaturedIPOs] = useState<IPO[]>([]);
  const [loadingIPOs, setLoadingIPOs] = useState(true);

  useEffect(() => {
    ipoService.getIPOs(undefined, undefined, undefined, undefined, 1, 3)
      .then(res => {
        setFeaturedIPOs(res.items);
        setLoadingIPOs(false);
      })
      .catch(err => {
        console.error('Failed to load featured IPOs:', err);
        setLoadingIPOs(false);
      });
  }, []);


  const faqs = [
    { q: 'What is IPO Genius AI?', a: 'IPO Genius AI is an advanced analysis platform that reviews draft red herring prospectuses (DRHP), financial sheets, and market sentiment to deliver accurate IPO scores, risks, and recommendations.' },
    { q: 'Is the AI analysis reliable?', a: 'Yes. Our AI engine uses machine learning and natural language processing models trained on historical financial data and IPO performances. However, it should only be used as a research assistant, not direct financial advice.' },
    { q: 'What is included in the Free plan?', a: 'The Free plan offers access to the IPO calendar, basic listing profiles, and 3 AI-generated analyses per month, along with standard email notifications.' },
    { q: 'How do I set up alerts?', a: 'Once registered, you can activate real-time email and Telegram notification triggers directly inside your dashboard settings panel.' },
    { q: 'Can I cancel my subscription anytime?', a: 'Absolutely. There are no lock-in contracts. You can downgrade or cancel your Pro Plan subscription at any time with one click from the billing tab.' }
  ];

  return (
    <div className="min-h-screen bg-dark-bg text-text-primary flex flex-col pt-16">
      <Navbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden py-24 px-6 md:px-12 flex flex-col items-center text-center max-w-6xl mx-auto">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-secondary-purple/10 rounded-full blur-[120px] pointer-events-none" />
        
        <div className="flex items-center gap-2 bg-gradient-to-r from-primary-blue/10 to-secondary-purple/10 border border-secondary-purple/20 px-4 py-1.5 rounded-full text-xs font-semibold text-secondary-purple mb-6 animate-pulse-glow">
          <Sparkles className="w-4 h-4" />
          <span>AI-Powered IPO Research Platform</span>
        </div>

        <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-white mb-6 max-w-4xl leading-tight">
          Invest Smarter with <span className="bg-gradient-to-r from-primary-blue via-secondary-purple to-accent-emerald bg-clip-text text-transparent">AI-Powered</span> IPO Insights
        </h1>

        <p className="text-lg text-text-secondary max-w-2xl mb-10 leading-relaxed">
          Get automated financial analysis, SWOT profiles, risk scores, and real-time alerts for every IPO, helping you separate gems from traps.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 mb-16">
          <Link href="/register" className="bg-primary-blue hover:bg-blue-700 text-white font-semibold px-8 py-3.5 rounded-md shadow-lg shadow-primary-blue/20 flex items-center gap-2 transition-all">
            Get Started Free <ArrowRight className="w-4 h-4" />
          </Link>
          <Link href="/features" className="border border-border-subtle hover:bg-card-bg text-white font-medium px-8 py-3.5 rounded-md transition-all">
            Explore Features
          </Link>
        </div>

        {/* Dashboard Mockup Preview */}
        <div className="w-full relative rounded-lg border border-border-subtle bg-sidebar-bg/60 p-4 shadow-2xl">
          <div className="h-6 w-full flex items-center gap-1.5 px-2 border-b border-border-subtle/50 pb-3 mb-4">
            <span className="w-2.5 h-2.5 rounded-full bg-red-500/80" />
            <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/80" />
            <span className="w-2.5 h-2.5 rounded-full bg-green-500/80" />
            <span className="text-[10px] text-text-muted ml-2 font-mono">ipogenius.ai/dashboard</span>
          </div>
          <div className="aspect-[16/9] bg-dark-bg rounded-md flex items-center justify-center border border-border-subtle p-6 overflow-hidden">
            <div className="w-full max-w-2xl bg-card-bg border border-border-strong rounded-lg p-6 text-left">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h4 className="text-lg font-bold text-white">Swiggy Limited</h4>
                  <span className="text-xs text-text-muted">Sector: FMCG & Quick Commerce</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-xs font-bold text-accent-emerald bg-accent-emerald/10 border border-accent-emerald/20 px-2 py-0.5 rounded-sm">OPEN</span>
                  <div className="w-12 h-12 rounded-full border-2 border-accent-emerald flex items-center justify-center font-bold text-accent-emerald text-sm">87</div>
                </div>
              </div>
              
              {/* SWOT Mini Preview */}
              <div className="grid grid-cols-2 gap-4 mb-4 text-xs">
                <div className="p-3 bg-emerald-500/5 border border-accent-emerald/20 rounded-md">
                  <h5 className="font-bold text-accent-emerald mb-1">Strengths</h5>
                  <p className="text-text-secondary leading-relaxed">Leading position in food delivery and quick commerce cohorts.</p>
                </div>
                <div className="p-3 bg-red-500/5 border border-red-500/20 rounded-md">
                  <h5 className="font-bold text-red-400 mb-1">Risks</h5>
                  <p className="text-text-secondary leading-relaxed">Intense competition and historical cash burn models.</p>
                </div>
              </div>

              {/* Progress bar preview */}
              <div className="space-y-1.5 text-xs">
                <div className="flex justify-between font-semibold">
                  <span className="text-text-secondary">AI Confidence Index</span>
                  <span className="text-secondary-purple">87%</span>
                </div>
                <div className="w-full h-2 bg-dark-bg rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-primary-blue to-secondary-purple rounded-full" style={{ width: '87%' }} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Trusted By Section */}
      <section className="bg-sidebar-bg border-t border-b border-border-subtle py-12 px-6">
        <div className="max-w-6xl mx-auto flex flex-col items-center text-center">
          <span className="text-xs font-bold tracking-widest text-text-muted mb-8 uppercase">TRUSTED BY OVER 10,000+ RETAIL INVESTORS</span>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 w-full max-w-4xl text-white">
            <div>
              <h3 className="text-3xl font-extrabold text-white mb-1">10,000+</h3>
              <p className="text-xs text-text-muted">Registered Users</p>
            </div>
            <div>
              <h3 className="text-3xl font-extrabold text-white mb-1">500+</h3>
              <p className="text-xs text-text-muted">IPOs Analyzed</p>
            </div>
            <div>
              <h3 className="text-3xl font-extrabold text-white mb-1">4.9 / 5</h3>
              <p className="text-xs text-text-muted">App Store Rating</p>
            </div>
            <div>
              <h3 className="text-3xl font-extrabold text-white mb-1">₹2 Cr+</h3>
              <p className="text-xs text-text-muted">Capital Allocated</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-24 px-6 max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-white mb-4">Complete IPO Analysis Suite</h2>
          <p className="text-text-secondary max-w-xl mx-auto">Powerful modules and automated crawlers working together to keep you ahead of the market.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            { title: 'AI Analysis', icon: Sparkles, color: 'text-secondary-purple', text: 'Deep machine learning scans of DRHP prospectuses generating instant strength lists, weaknesses, and a consolidated score.' },
            { title: 'IPO Calendar', icon: Calendar, color: 'text-primary-blue', text: 'Never miss an event. Live schedules detailing opening dates, bidding frames, allotment dates, and list day timelines.' },
            { title: 'Track Watchlists', icon: Star, color: 'text-accent-emerald', text: 'Bookmark your preferred listings. Monitor real-time gray market premiums (GMP) and subscription updates on the go.' },
            { title: 'AI Assistant Chat', icon: MessageSquare, color: 'text-secondary-purple', text: 'Converse directly with our AI assistant. Ask specific questions about debt ratios, executive board members, or promoter histories.' },
            { title: 'Instant Broadcasts', icon: Bell, color: 'text-primary-blue', text: 'Real-time automation pipelines sending opening reminders, closing flags, and listing price updates to your email and Telegram.' },
            { title: 'Structured Reports', icon: Layers, color: 'text-accent-emerald', text: 'Consolidated PDF summaries detailing corporate structures, business models, historical peer valuations, and audit assessments.' }
          ].map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <div key={idx} className="p-6 rounded-lg bg-card-bg border border-border-strong hover:border-primary-blue/30 transition-all flex flex-col gap-4">
                <div className={`p-2.5 rounded-md bg-dark-bg/60 w-fit ${feat.color}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="text-lg font-bold text-white">{feat.title}</h3>
                <p className="text-sm text-text-secondary leading-relaxed">{feat.text}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* How it Works Section */}
      <section className="bg-sidebar-bg/40 border-t border-b border-border-subtle py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-white mb-4">How It Works</h2>
            <p className="text-text-secondary max-w-xl mx-auto">Four simple steps to premium financial decision making.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative">
            {[
              { step: '01', title: 'Discover', desc: 'Browse our live calendar tracking all active, upcoming, and draft IPO filings.' },
              { step: '02', title: 'Read AI Review', desc: 'Scan AI scores, SWOT matrices, risk flags, and consolidated prospectuses.' },
              { step: '03', title: 'Track Progress', desc: 'Add selected listings to your watchlist and receive live price updates and GMPs.' },
              { step: '04', title: 'Invest Smarter', desc: 'Apply with confidence backed by institutional-grade research models.' }
            ].map((step, idx) => (
              <div key={idx} className="p-6 rounded-lg bg-dark-bg/50 border border-border-strong relative flex flex-col gap-3">
                <span className="text-3xl font-extrabold text-primary-blue/20 absolute right-6 top-6">{step.step}</span>
                <h3 className="text-lg font-bold text-white mt-4">{step.title}</h3>
                <p className="text-sm text-text-secondary leading-relaxed">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured IPOs List */}
      <section className="py-24 px-6 max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row items-start md:items-end justify-between mb-12">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2">Live IPO Analysis</h2>
            <p className="text-text-secondary">Explore draft ratings and live indices generated by our AI core.</p>
          </div>
          <Link href="/dashboard/ipo" className="text-sm font-semibold text-primary-blue hover:underline flex items-center gap-1.5 mt-4 md:mt-0">
            View All IPO Listings <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {loadingIPOs ? (
            [1, 2, 3].map((i) => (
              <div key={i} className="p-6 rounded-lg bg-card-bg border border-border-strong animate-pulse h-96" />
            ))
          ) : featuredIPOs.length > 0 ? (
            featuredIPOs.map((ipo) => (
              <div key={ipo.id} className="p-6 rounded-lg bg-card-bg border border-border-strong hover:border-secondary-purple/20 transition-all flex flex-col justify-between h-96">
                <div>
                  <div className="flex items-center justify-between mb-6">
                    <div className="w-10 h-10 rounded-md bg-gradient-to-br from-primary-blue/10 to-secondary-purple/10 flex items-center justify-center font-bold text-primary-blue">
                      {ipo.name.charAt(0)}
                    </div>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      ipo.status === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20' :
                      ipo.status === 'Upcoming' ? 'bg-primary-blue/10 text-primary-blue border border-primary-blue/20' :
                      'bg-dark-bg text-text-muted border border-border-subtle'
                    }`}>
                      {ipo.status.toUpperCase()}
                    </span>
                  </div>
                  
                  <h3 className="text-lg font-bold text-white mb-1">{ipo.name}</h3>
                  <span className="text-xs text-text-muted font-mono">{ipo.sector}</span>
                  
                  <div className="grid grid-cols-2 gap-4 mt-6 text-xs border-t border-border-subtle/40 pt-4 font-mono">
                    <div>
                      <span className="text-text-muted block mb-0.5">PRICE BAND</span>
                      <span className="font-bold text-white">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</span>
                    </div>
                    <div>
                      <span className="text-text-muted block mb-0.5">LOT SIZE</span>
                      <span className="font-bold text-white">{ipo.lotSize} Shares</span>
                    </div>
                  </div>
                </div>

                <Link href={`/dashboard/ipo/${ipo.id}`} className="mt-6 w-full bg-dark-bg hover:bg-card-bg border border-border-subtle hover:border-primary-blue/40 text-text-primary text-xs font-semibold py-2.5 rounded-md flex items-center justify-center gap-1 transition-all">
                  View Full Detail <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            ))
          ) : (
            <div className="col-span-3 py-12 text-center bg-card-bg border border-border-strong rounded-lg">
              <span className="text-xs text-text-muted">No IPOs currently featured.</span>
            </div>
          )}
        </div>
      </section>


      {/* Pricing Section */}
      <section className="py-24 px-6 bg-sidebar-bg/20 border-t border-b border-border-subtle">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-white mb-4">Simple, Transparent Pricing</h2>
          <p className="text-text-secondary max-w-xl mx-auto mb-8">Start free. Upgrade when you are ready. Cancel anytime.</p>

          <div className="flex items-center justify-center gap-3 mb-16">
            <span className={`text-sm ${billingCycle === 'monthly' ? 'text-white font-bold' : 'text-text-muted'}`}>Monthly</span>
            <button
              onClick={() => setBillingCycle(prev => prev === 'monthly' ? 'yearly' : 'monthly')}
              className="w-12 h-6 rounded-full bg-border-subtle p-0.5 relative transition-colors"
            >
              <div className={`w-5 h-5 rounded-full bg-primary-blue transition-all ${billingCycle === 'yearly' ? 'translate-x-6' : ''}`} />
            </button>
            <span className={`text-sm ${billingCycle === 'yearly' ? 'text-white font-bold' : 'text-text-muted'} flex items-center gap-1.5`}>
              Yearly
              <span className="text-[10px] font-bold bg-accent-emerald/20 text-accent-emerald px-1.5 py-0.5 rounded-sm">-20%</span>
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto text-left">
            {/* Free */}
            <div className="p-8 rounded-lg bg-card-bg border border-border-strong flex flex-col justify-between">
              <div>
                <span className="text-xs font-bold text-text-muted tracking-wider block mb-2 uppercase">FREE FOREVER</span>
                <h3 className="text-3xl font-extrabold text-white mb-6">₹0 <span className="text-sm font-normal text-text-muted">/ month</span></h3>
                <ul className="space-y-3.5 text-sm text-text-secondary">
                  <li className="flex items-center gap-2">✓ Browse all upcoming IPOs</li>
                  <li className="flex items-center gap-2">✓ Basic IPO profile metadata</li>
                  <li className="flex items-center gap-2">✓ 3 AI analyses per month</li>
                  <li className="flex items-center gap-2">✓ Email notifications</li>
                </ul>
              </div>
              <Link href="/register" className="mt-8 w-full border border-border-subtle hover:bg-dark-bg text-white font-semibold py-2.5 rounded-md text-center block transition-colors">
                Sign Up Free
              </Link>
            </div>

            {/* Pro */}
            <div className="p-8 rounded-lg bg-card-bg border-2 border-primary-blue relative flex flex-col justify-between shadow-2xl animate-pulse-glow">
              <span className="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-gradient-to-r from-primary-blue to-secondary-purple text-white text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                MOST POPULAR
              </span>
              <div>
                <span className="text-xs font-bold text-primary-blue tracking-wider block mb-2 uppercase">PRO INVESTOR</span>
                <h3 className="text-3xl font-extrabold text-white mb-6">
                  {billingCycle === 'monthly' ? '₹499' : '₹399'} <span className="text-sm font-normal text-text-muted">/ month</span>
                </h3>
                <ul className="space-y-3.5 text-sm text-text-secondary">
                  <li className="flex items-center gap-2 font-semibold text-white">✓ Everything in Free</li>
                  <li className="flex items-center gap-2">✓ Unlimited AI-generated scores</li>
                  <li className="flex items-center gap-2">✓ Full SWOT & risk audits</li>
                  <li className="flex items-center gap-2">✓ Interactive AI Assistant Chat</li>
                  <li className="flex items-center gap-2">✓ Email & Telegram instant alerts</li>
                  <li className="flex items-center gap-2">✓ GMP and subscription indexing</li>
                </ul>
              </div>
              <Link href="/register" className="mt-8 w-full bg-primary-blue hover:bg-blue-700 text-white font-semibold py-2.5 rounded-md text-center block transition-colors">
                Upgrade to Pro
              </Link>
            </div>

            {/* Enterprise */}
            <div className="p-8 rounded-lg bg-card-bg border border-border-strong flex flex-col justify-between">
              <div>
                <span className="text-xs font-bold text-text-muted tracking-wider block mb-2 uppercase">CORPORATE</span>
                <h3 className="text-3xl font-extrabold text-white mb-6">Custom</h3>
                <ul className="space-y-3.5 text-sm text-text-secondary">
                  <li className="flex items-center gap-2">✓ All Pro features</li>
                  <li className="flex items-center gap-2">✓ API data integration endpoints</li>
                  <li className="flex items-center gap-2">✓ Dedicated account supervisor</li>
                  <li className="flex items-center gap-2">✓ White-labeled report exports</li>
                </ul>
              </div>
              <Link href="/contact" className="mt-8 w-full border border-border-subtle hover:bg-dark-bg text-white font-semibold py-2.5 rounded-md text-center block transition-colors">
                Contact Sales
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Accordion Section */}
      <section className="py-24 px-6 max-w-3xl mx-auto w-full">
        <h2 className="text-3xl font-bold text-white text-center mb-12">Frequently Asked Questions</h2>
        <div className="space-y-4">
          {faqs.map((faq, idx) => (
            <div key={idx} className="border border-border-strong rounded-lg overflow-hidden bg-card-bg/30">
              <button
                onClick={() => setOpenFaq(prev => prev === idx ? null : idx)}
                className="w-full flex items-center justify-between p-5 text-left font-semibold text-white focus:outline-none"
              >
                <span>{faq.q}</span>
                <ChevronDown className={`w-4 h-4 text-text-muted transition-transform ${openFaq === idx ? 'rotate-180' : ''}`} />
              </button>
              {openFaq === idx && (
                <div className="px-5 pb-5 text-sm text-text-secondary leading-relaxed border-t border-border-strong/50 pt-3">
                  {faq.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Newsletter */}
      <section className="bg-gradient-to-r from-primary-blue/5 to-secondary-purple/5 border-t border-border-subtle py-20 px-6 text-center">
        <div className="max-w-xl mx-auto flex flex-col gap-4">
          <h2 className="text-2xl md:text-3xl font-bold text-white">Never Miss an IPO</h2>
          <p className="text-sm text-text-secondary">Join 10,000+ investors and get analysis alerts directly in your inbox.</p>
          <div className="flex flex-col sm:flex-row gap-3 mt-4">
            <input
              type="email"
              placeholder="Enter your email"
              className="flex-1 px-4 py-3 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-sm focus:outline-none focus:ring-1 focus:ring-primary-blue transition-all"
            />
            <button className="bg-primary-blue hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-md text-sm transition-colors">
              Subscribe
            </button>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
