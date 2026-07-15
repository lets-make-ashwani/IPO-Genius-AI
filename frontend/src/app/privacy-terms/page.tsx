import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

export default function PrivacyTerms() {
  return (
    <div className="min-h-screen bg-dark-bg text-text-primary flex flex-col pt-16">
      <Navbar />

      <section className="py-20 px-6 max-w-4xl mx-auto w-full mb-16">
        <h1 className="text-3xl md:text-4xl font-extrabold text-white mb-2">
          Legal Terms & Privacy Policy
        </h1>
        <span className="text-xs text-text-muted block mb-12">Last Updated: December 2025</span>

        <div className="grid grid-cols-1 md:grid-cols-12 gap-12">
          {/* Side links */}
          <div className="md:col-span-3 space-y-4 hidden md:block">
            <h5 className="text-xs font-bold text-white uppercase tracking-wider">SECTIONS</h5>
            <ul className="space-y-2.5 text-sm text-text-muted">
              <li><a href="#privacy" className="hover:text-white transition-colors">Privacy Policy</a></li>
              <li><a href="#terms" className="hover:text-white transition-colors">Terms of Service</a></li>
              <li><a href="#disclaimer" className="hover:text-white transition-colors">AI Disclaimers</a></li>
            </ul>
          </div>

          {/* Legal Texts */}
          <div className="md:col-span-9 space-y-16 text-sm text-text-secondary leading-relaxed">
            {/* Privacy */}
            <div id="privacy" className="space-y-6">
              <h2 className="text-2xl font-bold text-white">Privacy Policy</h2>
              <p>
                At IPO Genius AI, we take your personal data privacy seriously. This policy describes how we collect, process, and protect your information when you register and subscribe to our services.
              </p>
              <h3 className="font-bold text-white text-base">1. Data We Collect</h3>
              <p>
                We collect your name, email address, profile credentials, and transaction identifiers. Passwords are saved under standard cryptographic hash encryption models. We never store credit card or bank details directly; all payments are processed securely via third-party providers (Razorpay).
              </p>
              <h3 className="font-bold text-white text-base">2. How We Use Data</h3>
              <p>
                Your contact details are processed to manage account access, send automated IPO notifications (email + Telegram), and fulfill Pro Plan subscriptions.
              </p>
            </div>

            {/* Terms */}
            <div id="terms" className="space-y-6 pt-12 border-t border-border-strong/50">
              <h2 className="text-2xl font-bold text-white">Terms of Service</h2>
              <p>
                By accessing or registering on our platform, you agree to comply with and be bound by these Terms of Service.
              </p>
              <h3 className="font-bold text-white text-base">1. Subscription Plans</h3>
              <p>
                Pro Plan billing occurs on a recurring basis. All payments are non-refundable unless a transaction dispute arises. Subscriptions can be canceled at any time.
              </p>
              <h3 className="font-bold text-white text-base">2. Prohibited Uses</h3>
              <p>
                Users are strictly prohibited from reverse engineering, scrap-extracting AI analysis databases, or utilizing API routes without corporate license permissions.
              </p>
            </div>

            {/* Disclaimer */}
            <div id="disclaimer" className="space-y-6 pt-12 border-t border-border-strong/50">
              <h2 className="text-2xl font-bold text-white">AI Disclaimers</h2>
              <p>
                All data, ratings, scores, SWOT analyses, and recommendations produced by our AI model are for educational and informational research purposes only.
              </p>
              <div className="p-4 bg-yellow-500/5 border border-yellow-500/20 rounded-md text-xs text-yellow-500 italic leading-relaxed">
                ⚠ IPO Genius AI is not a SEBI-registered investment advisor. Our AI analyses do not constitute financial advice, buying guides, or direct recommendations to purchase shares. Invest at your own risk.
              </div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
