'use client';

import { useState } from 'react';
import { 
  Plus, 
  Search, 
  Edit, 
  Trash2, 
  Upload, 
  Check, 
  X,
  FileText,
  AlertTriangle
} from 'lucide-react';
import { mockIPOs } from '../../../constants/mockData';
import { IPO } from '../../../types';
import { ipoService } from '../../../services/ipo.service';

export default function IPOManagement() {
  const [ipos, setIpos] = useState<IPO[]>(mockIPOs);
  const [search, setSearch] = useState('');
  
  // Editor Drawer state
  const [isEditing, setIsEditing] = useState(false);
  const [currentIpo, setCurrentIpo] = useState<Partial<IPO> | null>(null);
  const [saved, setSaved] = useState(false);

  const filteredIPOs = ipos.filter(
    (ipo) => ipo.name.toLowerCase().includes(search.toLowerCase()) || ipo.ticker.toLowerCase().includes(search.toLowerCase())
  );

  const handleEdit = (ipo: IPO) => {
    setCurrentIpo(ipo);
    setIsEditing(true);
  };

  const handleAdd = () => {
    setCurrentIpo({
      name: '',
      ticker: '',
      sector: '',
      status: 'Upcoming',
      priceBand: { min: 0, max: 0 },
      issueSize: 0,
      lotSize: 0,
      openDate: '',
      closeDate: '',
      allotmentDate: '',
      refundDate: '',
      listingDate: '',
      gmp: 0,
      overview: '',
      businessModel: '',
      strengths: [],
      risks: [],
      swot: { strengths: [], weaknesses: [], opportunities: [], threats: [] },
      financialSummary: { years: ['FY23', 'FY24', 'FY25'], revenue: [0, 0, 0], profit: [0, 0, 0], ebitda: [0, 0, 0] }
    });
    setIsEditing(true);
  };

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this IPO listing?')) {
      await ipoService.deleteIPO(id);
      setIpos((prev) => prev.filter((i) => i.id !== id));
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentIpo) return;

    if (currentIpo.id) {
      // Update
      const updated = await ipoService.updateIPO(currentIpo.id, currentIpo);
      setIpos((prev) => prev.map((i) => (i.id === currentIpo.id ? updated : i)));
    } else {
      // Create
      const created = await ipoService.createIPO(currentIpo as any);
      setIpos((prev) => [created, ...prev]);
    }

    setSaved(true);
    setTimeout(() => {
      setSaved(false);
      setIsEditing(false);
      setCurrentIpo(null);
    }, 1000);
  };

  return (
    <div className="space-y-6 relative">
      
      {/* Title Header */}
      <div className="flex justify-between items-center border-b border-border-strong pb-3">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">IPO Management</h1>
          <p className="text-xs text-text-muted">Create, edit, and publish Red Herring Prospectus IPO data.</p>
        </div>
        <button
          onClick={handleAdd}
          className="bg-primary-blue hover:bg-blue-700 text-white font-semibold text-xs px-4 py-2.5 rounded-md flex items-center gap-1.5 shadow-md transition-colors"
        >
          <Plus className="w-4 h-4" /> Add New IPO
        </button>
      </div>

      {/* Directory Table */}
      <div className="space-y-4">
        {/* Controls */}
        <div className="relative w-80">
          <Search className="absolute left-3 top-3 w-4 h-4 text-text-muted" />
          <input
            type="text"
            placeholder="Search active listings..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full h-10 pl-10 pr-4 rounded-md bg-card-bg border border-border-subtle focus:border-primary-blue text-xs focus:outline-none text-white focus:ring-1 focus:ring-primary-blue transition-all"
          />
        </div>

        <div className="bg-card-bg border border-border-strong rounded-lg overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-border-strong bg-dark-bg/40 font-bold text-text-muted uppercase tracking-wider">
                <th className="p-4 pl-6">Company</th>
                <th className="p-4">Ticker</th>
                <th className="p-4">Price Band</th>
                <th className="p-4">Issue Size</th>
                <th className="p-4">Status</th>
                <th className="p-4">AI Score</th>
                <th className="p-4 pr-6 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="text-text-secondary divide-y divide-border-strong/30">
              {filteredIPOs.map((ipo) => (
                <tr key={ipo.id} className="hover:bg-dark-bg/25 transition-colors">
                  <td className="p-4 pl-6 font-bold text-white">{ipo.name}</td>
                  <td className="p-4 font-mono font-semibold">{ipo.ticker}</td>
                  <td className="p-4 font-mono">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</td>
                  <td className="p-4 font-mono">₹{ipo.issueSize} Cr</td>
                  <td className="p-4">
                    <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full ${
                      ipo.status === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald' : 'bg-primary-blue/10 text-primary-blue'
                    }`}>{ipo.status.toUpperCase()}</span>
                  </td>
                  <td className="p-4 font-mono font-semibold text-white">{ipo.aiScore}</td>
                  <td className="p-4 pr-6 text-right flex justify-end gap-3">
                    <button onClick={() => handleEdit(ipo)} className="p-1.5 rounded hover:bg-border-subtle text-text-muted hover:text-white transition-colors" title="Edit listing"><Edit className="w-4 h-4" /></button>
                    <button onClick={() => handleDelete(ipo.id)} className="p-1.5 rounded hover:bg-red-500/10 text-text-muted hover:text-red-400 transition-colors" title="Delete listing"><Trash2 className="w-4 h-4" /></button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Editor Side Panel overlay drawer */}
      {isEditing && currentIpo && (
        <div className="fixed inset-0 bg-black/60 z-50 flex justify-end">
          <div className="w-full max-w-xl bg-card-bg border-l border-border-strong h-full flex flex-col justify-between p-6 overflow-y-auto">
            <form onSubmit={handleSave} className="space-y-6">
              
              <div className="flex justify-between items-center border-b border-border-strong pb-4">
                <h3 className="font-bold text-white text-base">
                  {currentIpo.id ? `Edit IPO: ${currentIpo.name}` : 'Create New IPO Listing'}
                </h3>
                <button type="button" onClick={() => { setIsEditing(false); setCurrentIpo(null); }} className="p-1 rounded hover:bg-border-subtle text-text-muted hover:text-white"><X className="w-5 h-5" /></button>
              </div>

              {saved && (
                <div className="p-3 bg-accent-emerald/10 border border-accent-emerald/20 text-accent-emerald rounded-md text-xs flex items-center gap-2">
                  <Check className="w-4 h-4" /> Listing persistent changes updated!
                </div>
              )}

              {/* Form sections */}
              <div className="space-y-6 text-xs text-text-secondary">
                
                {/* Section 1 */}
                <div className="space-y-4">
                  <h4 className="font-bold text-white text-xs uppercase tracking-wider text-text-muted">Company Details</h4>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-1.5">
                      <label className="font-semibold text-text-muted uppercase">Company Name</label>
                      <input required type="text" value={currentIpo.name || ''} onChange={(e) => setCurrentIpo(p => ({ ...p, name: e.target.value }))} className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue focus:outline-none focus:ring-1 focus:ring-primary-blue text-white" />
                    </div>
                    <div className="space-y-1.5">
                      <label className="font-semibold text-text-muted uppercase">Ticker Symbol</label>
                      <input required type="text" value={currentIpo.ticker || ''} onChange={(e) => setCurrentIpo(p => ({ ...p, ticker: e.target.value }))} className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue focus:outline-none focus:ring-1 focus:ring-primary-blue text-white font-mono" />
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <label className="font-semibold text-text-muted uppercase">Sector Description</label>
                    <input required type="text" value={currentIpo.sector || ''} onChange={(e) => setCurrentIpo(p => ({ ...p, sector: e.target.value }))} className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue focus:outline-none focus:ring-1 focus:ring-primary-blue text-white" />
                  </div>
                </div>

                {/* Section 2 */}
                <div className="space-y-4 border-t border-border-strong/50 pt-4">
                  <h4 className="font-bold text-white text-xs uppercase tracking-wider text-text-muted">Financial Indicators</h4>
                  
                  <div className="grid grid-cols-3 gap-4">
                    <div className="space-y-1.5">
                      <label className="font-semibold text-text-muted uppercase">Issue Size (₹ Cr)</label>
                      <input required type="number" value={currentIpo.issueSize || 0} onChange={(e) => setCurrentIpo(p => p ? ({ ...p, issueSize: Number(e.target.value) }) : null)} className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue focus:outline-none focus:ring-1 focus:ring-primary-blue text-white font-mono" />
                    </div>
                    <div className="space-y-1.5">
                      <label className="font-semibold text-text-muted uppercase">Min Price (₹)</label>
                      <input required type="number" value={currentIpo.priceBand?.min || 0} onChange={(e) => setCurrentIpo(p => p ? ({ ...p, priceBand: { min: Number(e.target.value), max: p.priceBand?.max || 0 } }) : null)} className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue focus:outline-none focus:ring-1 focus:ring-primary-blue text-white font-mono" />
                    </div>
                    <div className="space-y-1.5">
                      <label className="font-semibold text-text-muted uppercase">Max Price (₹)</label>
                      <input required type="number" value={currentIpo.priceBand?.max || 0} onChange={(e) => setCurrentIpo(p => p ? ({ ...p, priceBand: { min: p.priceBand?.min || 0, max: Number(e.target.value) } }) : null)} className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue focus:outline-none focus:ring-1 focus:ring-primary-blue text-white font-mono" />
                    </div>
                  </div>
                </div>

                {/* Section 3 */}
                <div className="space-y-4 border-t border-border-strong/50 pt-4">
                  <h4 className="font-bold text-white text-xs uppercase tracking-wider text-text-muted">Bidding Timeline</h4>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-1.5">
                      <label className="font-semibold text-text-muted uppercase">Opening Date</label>
                      <input type="date" value={currentIpo.openDate || ''} onChange={(e) => setCurrentIpo(p => ({ ...p, openDate: e.target.value }))} className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue focus:outline-none focus:ring-1 focus:ring-primary-blue text-text-secondary font-mono" />
                    </div>
                    <div className="space-y-1.5">
                      <label className="font-semibold text-text-muted uppercase">Closing Date</label>
                      <input type="date" value={currentIpo.closeDate || ''} onChange={(e) => setCurrentIpo(p => ({ ...p, closeDate: e.target.value }))} className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue focus:outline-none focus:ring-1 focus:ring-primary-blue text-text-secondary font-mono" />
                    </div>
                  </div>
                </div>

                {/* DRHP Upload */}
                <div className="space-y-1.5 border-t border-border-strong/50 pt-4">
                  <label className="font-bold text-white text-xs uppercase tracking-wider text-text-muted">Prospectus DRHP Document</label>
                  <div className="w-full border-2 border-dashed border-border-subtle hover:border-primary-blue rounded-lg p-6 text-center bg-dark-bg/40 cursor-pointer transition-colors space-y-2 flex flex-col items-center justify-center">
                    <Upload className="w-6 h-6 text-text-muted" />
                    <span className="font-semibold text-xs text-white">Upload DRHP prospectus files</span>
                    <span className="text-[10px] text-text-muted">Support PDF files up to 25MB</span>
                  </div>
                </div>

              </div>

              <div className="flex justify-end gap-3 pt-6 border-t border-border-strong mt-8">
                <button type="button" onClick={() => { setIsEditing(false); setCurrentIpo(null); }} className="h-10 px-4 rounded border border-border-subtle hover:bg-dark-bg text-xs font-semibold text-white transition-colors">Cancel</button>
                <button type="submit" className="h-10 px-6 rounded bg-primary-blue hover:bg-blue-700 text-white font-semibold text-xs shadow-md transition-colors">Save Listing</button>
              </div>

            </form>
          </div>
        </div>
      )}

    </div>
  );
}
