import { IPO } from '../types';
import { mockIPOs } from '../constants/mockData';

// Simulated in-memory database for mock state persistence
let ipoList: IPO[] = [...mockIPOs];

export const ipoService = {
  getIPOs: async (search?: string, status?: string, sector?: string): Promise<IPO[]> => {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 300));
    
    let filtered = [...ipoList];
    
    if (search) {
      const s = search.toLowerCase();
      filtered = filtered.filter(
        (ipo) =>
          ipo.name.toLowerCase().includes(s) ||
          ipo.ticker.toLowerCase().includes(s) ||
          ipo.sector.toLowerCase().includes(s)
      );
    }
    
    if (status && status !== 'All') {
      filtered = filtered.filter((ipo) => ipo.status.toLowerCase() === status.toLowerCase());
    }
    
    if (sector && sector !== 'All') {
      filtered = filtered.filter((ipo) => ipo.sector.toLowerCase().includes(sector.toLowerCase()));
    }
    
    return filtered;
  },

  getIPOById: async (id: string): Promise<IPO | undefined> => {
    await new Promise((resolve) => setTimeout(resolve, 200));
    return ipoList.find((ipo) => ipo.id === id);
  },

  createIPO: async (ipo: Omit<IPO, 'id' | 'aiScore' | 'aiRecommendation'>): Promise<IPO> => {
    await new Promise((resolve) => setTimeout(resolve, 500));
    const newIPO: IPO = {
      ...ipo,
      id: ipo.name.toLowerCase().replace(/ /g, '-'),
      aiScore: Math.floor(Math.random() * 30) + 60, // random score 60-90
      aiRecommendation: 'Buy'
    };
    ipoList = [newIPO, ...ipoList];
    return newIPO;
  },

  updateIPO: async (id: string, updated: Partial<IPO>): Promise<IPO> => {
    await new Promise((resolve) => setTimeout(resolve, 400));
    ipoList = ipoList.map((ipo) => (ipo.id === id ? { ...ipo, ...updated } : ipo));
    const found = ipoList.find((ipo) => ipo.id === id);
    if (!found) throw new Error('IPO not found');
    return found;
  },

  deleteIPO: async (id: string): Promise<boolean> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    const exists = ipoList.some((ipo) => ipo.id === id);
    ipoList = ipoList.filter((ipo) => ipo.id !== id);
    return exists;
  },

  triggerAIAnalysis: async (id: string): Promise<IPO> => {
    await new Promise((resolve) => setTimeout(resolve, 1500)); // longer AI latency simulation
    const ipo = ipoList.find((i) => i.id === id);
    if (!ipo) throw new Error('IPO not found');
    
    const newScore = Math.floor(Math.random() * 20) + 75; // 75-95 score
    const recs: IPO['aiRecommendation'][] = ['Strong Buy', 'Buy', 'Hold'];
    const newRec = recs[Math.floor(Math.random() * recs.length)];
    
    return ipoService.updateIPO(id, {
      aiScore: newScore,
      aiRecommendation: newRec
    });
  }
};
