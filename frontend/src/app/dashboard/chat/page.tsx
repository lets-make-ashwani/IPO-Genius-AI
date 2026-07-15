'use client';

import { useState, useRef, useEffect } from 'react';
import { 
  Sparkles, 
  Send, 
  Paperclip, 
  Mic, 
  MessageSquare, 
  PlusCircle, 
  ThumbsUp, 
  ThumbsDown, 
  Copy,
  ChevronRight,
  TrendingUp
} from 'lucide-react';
import { ChatMessage } from '../../../types';

export default function AIChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { id: 'm1', sender: 'ai', text: 'Hello! I am your IPO Genius AI research companion. Ask me anything about upcoming prospectuses, cash flow records, or valuation multiples.', timestamp: '2:30 PM' }
  ]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const [activeChat, setActiveChat] = useState('swiggy-ipo');

  const recentChats = [
    { id: 'swiggy-ipo', title: 'Tell me about Swiggy IPO', time: '2h ago' },
    { id: 'ola-electric', title: 'Ola Electric vs Bajaj Housing', time: '1d ago' },
    { id: 'gmp-meaning', title: 'What is GMP meaning?', time: '3d ago' },
    { id: 'best-ipo', title: 'Best IPOs this month', time: '1w ago' }
  ];

  const suggestedQuestions = [
    'What is the AI Score for Swiggy?',
    'Explain the SWOT analysis for Swiggy',
    'Ola Electric vs Bajaj Housing: which is better?',
    'What is the GMP today for upcoming IPOs?'
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isThinking]);

  const handleSendMessage = (text: string) => {
    if (!text.trim()) return;

    const userMsg: ChatMessage = {
      id: 'msg-' + Math.random(),
      sender: 'user',
      text,
      timestamp: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsThinking(true);

    // Simulate AI response delay
    setTimeout(() => {
      let aiText = `Based on current prospectuses, here are details for your query.`;
      let aiScore: number | undefined = undefined;

      const lowerText = text.toLowerCase();
      if (lowerText.includes('swiggy') && lowerText.includes('score')) {
        aiText = 'Swiggy Limited has an AI Score of **87/100**, indicating a **Strong Buy** recommendation. The company shows high customer cohort retention rates and quick-commerce market consolidation.';
        aiScore = 87;
      } else if (lowerText.includes('swot') && lowerText.includes('swiggy')) {
        aiText = 'Swiggy SWOT Profile:\n\n• **Strengths**: Large customer cohort base, dual-brand ecosystem, path to profitability.\n• **Weaknesses**: Historical net losses, thin quick-commerce margins.\n• **Opportunities**: Tier 3/4 expansion, private labels, ad monetization.\n• **Threats**: Zomato/Zepto pricing pressure, rising delivery partner costs.';
      } else if (lowerText.includes('ola') && lowerText.includes('bajaj')) {
        aiText = 'Comparing Ola Electric vs. Bajaj Housing Finance:\n\n• **Bajaj Housing** (AI Score: **94**): Exceptional AAA rating, lowest GNPA (0.3%), safe listing with high GMP premium (+110%).\n• **Ola Electric** (AI Score: **74**): Leading EV player but capital intensive, product reliability issues, and cash burn. Buy for secondary growth.';
      } else if (lowerText.includes('gmp')) {
        aiText = 'Grey Market Premium (GMP) represents the unofficial premium at which an IPO is traded before listing. Bajaj Housing had a peak GMP of +110%, while Swiggy is currently trading at a modest +12% premium.';
      } else {
        aiText = 'I have reviewed your query against current SEBI draft prospectuses. Could you specify which company ticker or sector valuation multiple you would like me to audit?';
      }

      const aiMsg: ChatMessage = {
        id: 'msg-' + Math.random(),
        sender: 'ai',
        text: aiText,
        timestamp: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
        aiScore
      };

      setMessages((prev) => [...prev, aiMsg]);
      setIsThinking(false);
    }, 1200);
  };

  return (
    <div className="h-[calc(100vh-140px)] flex border border-border-strong bg-card-bg/20 rounded-lg overflow-hidden">
      
      {/* Left Chat History Sidebar */}
      <div className="w-64 bg-sidebar-bg border-r border-border-strong flex flex-col justify-between p-4 hidden md:flex shrink-0">
        <div className="space-y-4">
          <button className="w-full h-10 border border-dashed border-border-subtle hover:border-primary-blue hover:text-white rounded-md flex items-center justify-center gap-2 text-xs font-semibold text-text-secondary transition-colors">
            <PlusCircle className="w-4 h-4" /> New Chat
          </button>
          
          <div className="space-y-2">
            <h5 className="text-[10px] font-bold text-text-muted uppercase tracking-wider px-2">Recent Conversations</h5>
            <div className="space-y-1">
              {recentChats.map((chat) => (
                <button
                  key={chat.id}
                  onClick={() => {
                    setActiveChat(chat.id);
                    setMessages([
                      { id: 'm1', sender: 'ai', text: `Let's discuss: "${chat.title}". Ask me about finances, promoter pledged shares, or GMP.`, timestamp: 'Just now' }
                    ]);
                  }}
                  className={`w-full text-left px-3 py-2 rounded-md text-xs font-medium transition-colors flex flex-col gap-1 ${
                    activeChat === chat.id 
                      ? 'bg-blue-600/10 text-primary-blue' 
                      : 'text-text-secondary hover:bg-card-bg/60 hover:text-white'
                  }`}
                >
                  <span className="truncate block font-semibold">{chat.title}</span>
                  <span className="text-[9px] text-text-muted">{chat.time}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="text-[10px] text-text-muted border-t border-border-strong pt-3">
          Context scope: SEBI DRHP Filings 2024-2026.
        </div>
      </div>

      {/* Right Chat Window */}
      <div className="flex-1 flex flex-col justify-between bg-dark-bg/25">
        {/* Top active bar */}
        <div className="h-14 border-b border-border-strong px-6 flex items-center justify-between bg-sidebar-bg/60">
          <div className="flex items-center gap-2">
            <div className="p-1 rounded bg-secondary-purple/15 text-secondary-purple">
              <Sparkles className="w-4 h-4" />
            </div>
            <span className="font-bold text-xs text-white">IPO Assistant Core</span>
            <span className="text-[9px] text-accent-emerald bg-accent-emerald/10 px-1.5 py-0.2 rounded-sm font-mono">ONLINE</span>
          </div>
          {activeChat && (
            <span className="text-[10px] text-text-muted hidden sm:inline-block">Context: Active IPO Analysis</span>
          )}
        </div>

        {/* Message area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map((msg) => (
            <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[75%] p-4 rounded-lg text-xs leading-relaxed space-y-3 ${
                msg.sender === 'user' 
                  ? 'bg-primary-blue text-white rounded-br-none shadow-md' 
                  : 'bg-card-bg border border-border-strong text-text-secondary rounded-bl-none shadow-xl'
              }`}>
                {msg.sender === 'ai' && (
                  <div className="flex items-center gap-1.5 text-[9px] font-bold text-text-muted mb-1">
                    <Sparkles className="w-3 h-3 text-secondary-purple" />
                    <span>IPO GENIUS AI</span>
                    <span>·</span>
                    <span>{msg.timestamp}</span>
                  </div>
                )}
                
                <p className="whitespace-pre-line">{msg.text}</p>
                
                {msg.aiScore && (
                  <div className="flex items-center gap-2 bg-dark-bg border border-border-subtle p-2 rounded-md mt-2 w-fit">
                    <div className="w-7 h-7 rounded-full border-2 border-accent-emerald text-accent-emerald font-bold text-[10px] flex items-center justify-center font-mono">
                      {msg.aiScore}
                    </div>
                    <div className="leading-none">
                      <span className="text-[9px] text-text-muted block">AI SCORE</span>
                      <span className="text-[10px] font-bold text-white">Strong Buy</span>
                    </div>
                  </div>
                )}

                {msg.sender === 'ai' && (
                  <div className="flex gap-3 pt-3 border-t border-border-subtle/20 text-text-muted">
                    <button className="hover:text-white transition-colors" title="Helpful"><ThumbsUp className="w-3.5 h-3.5" /></button>
                    <button className="hover:text-white transition-colors" title="Not helpful"><ThumbsDown className="w-3.5 h-3.5" /></button>
                    <button className="hover:text-white transition-colors ml-auto" title="Copy reply"><Copy className="w-3.5 h-3.5" /></button>
                  </div>
                )}
              </div>
            </div>
          ))}

          {isThinking && (
            <div className="flex justify-start">
              <div className="max-w-[75%] p-4 rounded-lg bg-card-bg border border-border-strong text-text-secondary rounded-bl-none shadow-xl flex items-center gap-2 text-xs">
                <div className="flex gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-secondary-purple animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-secondary-purple animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-secondary-purple animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
                <span className="text-text-muted italic">Genius is auditing prospectuses...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input & Suggested questions bar */}
        <div className="p-4 border-t border-border-strong bg-sidebar-bg/40 space-y-4">
          {/* Suggestions */}
          {messages.length === 1 && (
            <div className="flex flex-wrap gap-2">
              {suggestedQuestions.map((q) => (
                <button
                  key={q}
                  onClick={() => handleSendMessage(q)}
                  className="text-[10px] font-semibold bg-dark-bg/60 border border-border-subtle hover:border-primary-blue hover:text-white text-text-secondary px-3 py-1.5 rounded-full transition-colors text-left"
                >
                  {q}
                </button>
              ))}
            </div>
          )}

          {/* Form */}
          <div className="relative flex items-center bg-dark-bg border border-border-subtle rounded-md h-12 px-3">
            <button className="p-1 rounded-md text-text-muted hover:text-white transition-colors" title="Attach file">
              <Paperclip className="w-4 h-4" />
            </button>
            <input
              type="text"
              placeholder="Ask a question about any IPO (e.g. debt levels, promoters)..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage(input)}
              className="flex-1 h-full bg-transparent px-3 text-xs focus:outline-none text-white placeholder-text-muted"
            />
            <div className="flex gap-2 items-center">
              <button className="p-1 rounded-md text-text-muted hover:text-white transition-colors hidden sm:block" title="Voice prompt">
                <Mic className="w-4 h-4" />
              </button>
              <button
                onClick={() => handleSendMessage(input)}
                className="p-1.5 rounded bg-primary-blue hover:bg-blue-700 text-white transition-colors"
                title="Send"
              >
                <Send className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
          <span className="text-[9px] text-text-muted block text-center">AI responses may contain anomalies. Always verify against draft red herring prospectuses (DRHP).</span>
        </div>

      </div>
    </div>
  );
}
