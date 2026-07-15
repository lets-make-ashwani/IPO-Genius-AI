'use client';

import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { Mail, Phone, MapPin, Send } from 'lucide-react';
import { useState } from 'react';

export default function Contact() {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="min-h-screen bg-dark-bg text-text-primary flex flex-col pt-16">
      <Navbar />

      <section className="py-20 px-6 text-center max-w-4xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-6">
          Get in Touch
        </h1>
        <p className="text-lg text-text-secondary max-w-xl mx-auto">
          Have a question about our pricing, AI scoring model, or reports? Drop us a line.
        </p>
      </section>

      <section className="py-12 px-6 max-w-5xl mx-auto w-full grid grid-cols-1 md:grid-cols-12 gap-12 mb-20">
        {/* Contact Form */}
        <div className="md:col-span-7 bg-card-bg border border-border-strong p-8 rounded-lg shadow-xl">
          {submitted ? (
            <div className="text-center py-16 space-y-4">
              <div className="w-12 h-12 rounded-full bg-accent-emerald/20 text-accent-emerald flex items-center justify-center mx-auto text-xl">✓</div>
              <h3 className="text-lg font-bold text-white">Message Sent Successfully!</h3>
              <p className="text-sm text-text-secondary">We will get back to you within 24 business hours.</p>
              <button onClick={() => setSubmitted(false)} className="text-sm font-semibold text-primary-blue hover:underline">Send another message</button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              <h3 className="text-xl font-bold text-white mb-4">Send us a message</h3>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-text-muted uppercase">Full Name</label>
                  <input required type="text" placeholder="John Doe" className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-sm focus:outline-none focus:ring-1 focus:ring-primary-blue transition-all" />
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-text-muted uppercase">Email Address</label>
                  <input required type="email" placeholder="john@example.com" className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-sm focus:outline-none focus:ring-1 focus:ring-primary-blue transition-all" />
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold text-text-muted uppercase">Subject</label>
                <select className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-sm focus:outline-none focus:ring-1 focus:ring-primary-blue transition-all text-text-secondary">
                  <option>General Inquiry</option>
                  <option>Billing & Subscriptions</option>
                  <option>AI Engine Feedback</option>
                  <option>Partnerships / API Access</option>
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold text-text-muted uppercase">Message</label>
                <textarea required rows={5} placeholder="How can we help you?" className="w-full p-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-sm focus:outline-none focus:ring-1 focus:ring-primary-blue transition-all resize-none"></textarea>
              </div>

              <button type="submit" className="w-full bg-primary-blue hover:bg-blue-700 text-white font-semibold py-3 rounded-md text-sm transition-colors flex items-center justify-center gap-2">
                Send Message <Send className="w-4 h-4" />
              </button>
            </form>
          )}
        </div>

        {/* Contact Info */}
        <div className="md:col-span-5 space-y-6">
          <div className="p-6 bg-card-bg border border-border-strong rounded-lg flex gap-4 items-start">
            <div className="p-2.5 rounded-md bg-dark-bg/60 text-primary-blue shrink-0">
              <Mail className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-semibold text-white mb-1">Email Support</h4>
              <p className="text-sm text-text-secondary">support@ipogenius.ai</p>
              <span className="text-xs text-text-muted">Response within 24 hours</span>
            </div>
          </div>

          <div className="p-6 bg-card-bg border border-border-strong rounded-lg flex gap-4 items-start">
            <div className="p-2.5 rounded-md bg-dark-bg/60 text-primary-blue shrink-0">
              <Phone className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-semibold text-white mb-1">Call Us</h4>
              <p className="text-sm text-text-secondary">+91 98765 43210</p>
              <span className="text-xs text-text-muted">Mon-Fri, 9:00 AM - 6:00 PM IST</span>
            </div>
          </div>

          <div className="p-6 bg-card-bg border border-border-strong rounded-lg flex gap-4 items-start">
            <div className="p-2.5 rounded-md bg-dark-bg/60 text-primary-blue shrink-0">
              <MapPin className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-semibold text-white mb-1">HQ Address</h4>
              <p className="text-sm text-text-secondary">Bandra Kurla Complex, Mumbai, MH, India</p>
            </div>
          </div>

          <div className="w-full aspect-[4/3] bg-card-bg border border-border-strong rounded-lg flex items-center justify-center text-xs text-text-muted">
            Google Map Placeholder
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
