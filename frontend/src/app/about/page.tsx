import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { Target, Eye, ShieldCheck, Heart } from 'lucide-react';

export default function About() {
  const coreValues = [
    { icon: ShieldCheck, title: 'Transparency', desc: 'We deliver pure data-driven metrics directly sourced from official DRHP filings without bias.' },
    { icon: Target, title: 'Accuracy', desc: 'Our AI models are regularly benchmarked against historical IPO performance curves to keep insights precise.' },
    { icon: Eye, title: 'Visionary', desc: 'We democratize institutional-grade financial analysis tools for individual retail investors.' },
    { icon: Heart, title: 'Integrity', desc: 'We never accept sponsor placements or paid promotions to skew individual stock scores.' }
  ];

  return (
    <div className="min-h-screen bg-dark-bg text-text-primary flex flex-col pt-16">
      <Navbar />

      <section className="py-20 px-6 text-center max-w-4xl mx-auto">
        <span className="text-xs font-bold text-primary-blue bg-primary-blue/10 px-3.5 py-1.5 rounded-full uppercase tracking-wider mb-4 inline-block">
          Our Story
        </span>
        <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-6">
          Making IPO Investing Transparent for Everyone
        </h1>
        <p className="text-lg text-text-secondary max-w-2xl mx-auto">
          We believe every retail investor deserves clear, structured, and institutional-grade analysis before allocating capital.
        </p>
      </section>

      {/* Grid of Values */}
      <section className="py-12 px-6 max-w-5xl mx-auto w-full mb-20">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {coreValues.map((val, idx) => {
            const Icon = val.icon;
            return (
              <div key={idx} className="p-8 bg-card-bg border border-border-strong rounded-lg flex gap-5 items-start">
                <div className="p-3 bg-dark-bg/60 rounded-md text-primary-blue shrink-0">
                  <Icon className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white mb-2">{val.title}</h3>
                  <p className="text-sm text-text-secondary leading-relaxed">{val.desc}</p>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Timeline Section */}
      <section className="bg-sidebar-bg/40 border-t border-b border-border-subtle py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-2xl font-bold text-white mb-12">Our Journey</h2>
          <div className="space-y-8 relative before:absolute before:left-1/2 before:top-2 before:bottom-2 before:w-[2px] before:bg-border-strong text-left">
            {[
              { year: '2024', title: 'Platform Conception', desc: 'Founded by a team of finance analysts and AI engineers to solve the complexity of reading 400+ page prospectuses.' },
              { year: '2025', title: 'Core Scoring Release', desc: 'Deployed the first DRHP text crawler and semantic analysis model. Audited 200+ historical IPO listings.' },
              { year: '2026', title: '10k Users Milestone', desc: 'Opened the platform to the public. Helping over 10,000 retail traders evaluate upcoming IPO listings weekly.' }
            ].map((milestone, idx) => (
              <div key={idx} className="relative flex justify-between items-center w-full md:odd:flex-row-reverse">
                <div className="w-[45%] hidden md:block" />
                <div className="absolute left-1/2 -translate-x-1/2 w-4 h-4 rounded-full bg-primary-blue border-4 border-dark-bg z-10" />
                <div className="w-full md:w-[45%] bg-card-bg border border-border-strong p-6 rounded-lg">
                  <span className="text-primary-blue font-bold text-lg block mb-1">{milestone.year}</span>
                  <h4 className="font-bold text-white mb-2">{milestone.title}</h4>
                  <p className="text-xs text-text-secondary leading-relaxed">{milestone.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
