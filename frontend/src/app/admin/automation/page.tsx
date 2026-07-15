'use client';

import { useState } from 'react';
import { Sparkles, Bell, Send, Play, ShieldCheck, Activity, Cpu } from 'lucide-react';

export default function AutomationControl() {
  const [broadcastChannel, setBroadcastChannel] = useState('Email');
  const [broadcastTitle, setBroadcastTitle] = useState('');
  const [broadcastContent, setBroadcastContent] = useState('');
  const [sent, setSent] = useState(false);

  const [workflows, setWorkflows] = useState([
    { id: 'wf1', name: 'IPO DRHP Collector crawler', trigger: 'Daily Schedule', lastRun: '2026-07-15 08:00', status: 'Success' },
    { id: 'wf2', name: 'AI Analysis Generator', trigger: 'Webhook - New DRHP', lastRun: '2026-07-15 11:34', status: 'Success' },
    { id: 'wf3', name: 'Notification Broadcast engine', trigger: 'Bidding Window open/close', lastRun: '2026-07-15 13:00', status: 'Success' }
  ]);

  const handleBroadcast = (e: React.FormEvent) => {
    e.preventDefault();
    setSent(true);
    setTimeout(() => {
      setSent(false);
      setBroadcastTitle('');
      setBroadcastContent('');
    }, 2000);
  };

  const handleRunWorkflow = (id: string) => {
    setWorkflows(prev => prev.map(w => w.id === id ? { ...w, lastRun: 'Just now', status: 'Success' } : w));
    alert('Automation pipeline workflow triggered.');
  };

  return (
    <div className="space-y-8">
      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">System Automation & AI Engine</h1>
        <p className="text-xs text-text-muted">Control text models, n8n webhook nodes, and alert campaign broadcasts.</p>
      </div>

      {/* AI stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'Total Model Requests', val: '1,42,506', sub: 'Last 30 days', color: 'text-primary-blue' },
          { label: 'API Success Rate', val: '99.8%', sub: 'Avg 1.8s response time', color: 'text-accent-emerald' },
          { label: 'Failed Jobs Queue', val: '12', sub: 'Awaiting automatic retry', color: 'text-red-400' },
          { label: 'Max Token Limit', val: '4,096', sub: 'GPT-4o standard context', color: 'text-secondary-purple' }
        ].map((stat, idx) => (
          <div key={idx} className="p-6 bg-card-bg border border-border-strong rounded-lg">
            <span className="text-xs font-bold text-text-muted block mb-1 uppercase tracking-wider">{stat.label}</span>
            <span className={`text-3xl font-extrabold font-mono block ${stat.color}`}>{stat.val}</span>
            <span className="text-[10px] text-text-muted block mt-1.5">{stat.sub}</span>
          </div>
        ))}
      </div>

      {/* Split Panels */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Side: Broadcast alert */}
        <div className="lg:col-span-7 bg-card-bg border border-border-strong rounded-lg p-6 space-y-6">
          <h3 className="font-bold text-white text-sm flex items-center gap-2 border-b border-border-strong pb-3">
            <Bell className="w-4 h-4 text-primary-blue" /> Create Broadcast Campaign
          </h3>

          {sent && (
            <div className="p-3 bg-accent-emerald/10 border border-accent-emerald/20 text-accent-emerald rounded-md text-xs">
              ✓ Campaign alerts dispatched to selected broadcast channels.
            </div>
          )}

          <form onSubmit={handleBroadcast} className="space-y-4 text-xs">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="font-bold text-text-muted uppercase">Select Channel</label>
                <select
                  value={broadcastChannel}
                  onChange={(e) => setBroadcastChannel(e.target.value)}
                  className="w-full h-10 px-4 rounded bg-dark-bg border border-border-subtle focus:outline-none text-text-secondary focus:border-primary-blue"
                >
                  <option>Email</option>
                  <option>Telegram</option>
                  <option>Push Notifications</option>
                </select>
              </div>
              <div className="space-y-1.5">
                <label className="font-bold text-text-muted uppercase">Notification Title</label>
                <input required type="text" placeholder="Swiggy IPO opens tomorrow!" value={broadcastTitle} onChange={(e) => setBroadcastTitle(e.target.value)} className="w-full h-10 px-4 rounded bg-dark-bg border border-border-subtle focus:outline-none text-white focus:border-primary-blue" />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="font-bold text-text-muted uppercase">Alert Body Content</label>
              <textarea required rows={4} placeholder="Write alert notification content..." value={broadcastContent} onChange={(e) => setBroadcastContent(e.target.value)} className="w-full p-4 rounded bg-dark-bg border border-border-subtle focus:outline-none text-white focus:border-primary-blue resize-none"></textarea>
            </div>

            <button type="submit" className="bg-primary-blue hover:bg-blue-700 text-white font-semibold px-6 py-2.5 rounded-md shadow-md flex items-center gap-1.5 transition-colors">
              <Send className="w-4 h-4" /> Dispatch Alert
            </button>
          </form>
        </div>

        {/* Right Side: n8n pipelines */}
        <div className="lg:col-span-5 bg-card-bg border border-border-strong rounded-lg p-6 space-y-6">
          <h3 className="font-bold text-white text-sm flex items-center gap-2 border-b border-border-strong pb-3">
            <Cpu className="w-4 h-4 text-primary-blue" /> n8n Automation Workflows
          </h3>

          <div className="space-y-4">
            {workflows.map((wf) => (
              <div key={wf.id} className="p-4 rounded-md border border-border-subtle bg-dark-bg/60 flex items-start justify-between gap-4">
                <div className="text-left text-xs space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-white">{wf.name}</span>
                    <span className="text-[9px] font-bold bg-accent-emerald/20 text-accent-emerald px-1.5 py-0.2 rounded-sm">{wf.status}</span>
                  </div>
                  <span className="text-[10px] text-text-muted block">Trigger: {wf.trigger}</span>
                  <span className="text-[10px] text-text-muted font-mono block">Last Run: {wf.lastRun}</span>
                </div>
                
                <button
                  onClick={() => handleRunWorkflow(wf.id)}
                  className="p-1.5 rounded hover:bg-border-subtle text-text-muted hover:text-white transition-colors"
                  title="Run pipeline workflow manually"
                >
                  <Play className="w-3.5 h-3.5" />
                </button>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
