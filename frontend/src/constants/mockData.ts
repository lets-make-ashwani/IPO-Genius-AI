import { IPO, User, Transaction } from '../types';

export const mockUsers: User[] = [
  {
    id: 'u1',
    name: 'Rahul Kumar',
    email: 'rahul@example.com',
    avatar: 'RK',
    plan: 'Pro',
    status: 'Active',
    joinedDate: '12 Jan 2024'
  },
  {
    id: 'u2',
    name: 'Ashwani Vishwakarma',
    email: 'ashwani@example.com',
    avatar: 'AV',
    plan: 'Pro',
    status: 'Active',
    joinedDate: '28 Feb 2024'
  },
  {
    id: 'u3',
    name: 'Pooja Sharma',
    email: 'pooja@example.com',
    avatar: 'PS',
    plan: 'Free',
    status: 'Active',
    joinedDate: '15 Mar 2024'
  },
  {
    id: 'u4',
    name: 'Vikram Singh',
    email: 'vikram@example.com',
    avatar: 'VS',
    plan: 'Enterprise',
    status: 'Active',
    joinedDate: '01 Apr 2024'
  },
  {
    id: 'u5',
    name: 'Amit Patel',
    email: 'amit@example.com',
    avatar: 'AP',
    plan: 'Free',
    status: 'Blocked',
    joinedDate: '10 May 2024'
  }
];

export const mockIPOs: IPO[] = [
  {
    id: 'swiggy',
    name: 'Swiggy Limited',
    ticker: 'SWIGGY',
    sector: 'FMCG & Quick Commerce',
    status: 'Open',
    priceBand: { min: 371, max: 390 },
    issueSize: 11327,
    lotSize: 38,
    openDate: '2026-07-16',
    closeDate: '2026-07-18',
    allotmentDate: '2026-07-19',
    refundDate: '2026-07-20',
    listingDate: '2026-07-22',
    aiScore: 87,
    aiRecommendation: 'Strong Buy',
    gmp: 12,
    overview: 'Swiggy Limited is a leading consumer technology company in India, offering a comprehensive platform that covers food delivery, quick commerce, and out-of-home dining options. Founded in 2014, it connects millions of users with over 200,000 restaurant partners and grocery merchants.',
    businessModel: 'Swiggy operates a three-sided marketplace model connecting customers, restaurant/grocery merchants, and delivery partners. Revenue is generated from customer delivery fees, merchant commissions, advertising fees, and Swiggy One subscription programs.',
    financialSummary: {
      years: ['FY22', 'FY23', 'FY24'],
      revenue: [5705, 8263, 11247],
      profit: [-3628, -4179, -2350],
      ebitda: [-3120, -3450, -1850]
    },
    strengths: [
      'Leading positions in food delivery and quick commerce (Instamart).',
      'Strong brand recall and massive customer cohort base.',
      'Significant improvement in EBITDA margin and path to profitability.'
    ],
    risks: [
      'Intense competition with Zomato and Zepto.',
      'Historical cash burn and dependency on continuous tech investments.',
      'Regulatory compliance risks related to delivery partner gig-worker rules.'
    ],
    swot: {
      strengths: ['High user retention', 'Strong dual-brand ecosystem (Food + Instamart)', 'Expanding market reach'],
      weaknesses: ['Higher customer acquisition costs', 'Historical net losses', 'Thin margins in quick commerce'],
      opportunities: ['Expansion into Tier 3 & Tier 4 cities', 'Advertising revenue scaling', 'Private label brand monetization'],
      threats: ['Aggressive pricing by competitors', 'Rising fuel and delivery partner costs', 'Strict consumer protection regulations']
    }
  },
  {
    id: 'ola-electric',
    name: 'Ola Electric Mobility',
    ticker: 'OLAELEC',
    sector: 'Automobile & EV',
    status: 'Upcoming',
    priceBand: { min: 72, max: 76 },
    issueSize: 6145,
    lotSize: 195,
    openDate: '2026-07-21',
    closeDate: '2026-07-24',
    allotmentDate: '2026-07-25',
    refundDate: '2026-07-28',
    listingDate: '2026-07-30',
    aiScore: 74,
    aiRecommendation: 'Buy',
    gmp: 18,
    overview: 'Ola Electric is India\'s largest electric two-wheeler manufacturer, building vertically integrated technology and manufacturing capabilities for EVs. It operates the FutureFactory in Tamil Nadu, aiming to capture the massive transition of local transport to electric options.',
    businessModel: 'Vertical production of EV two-wheelers, battery packs, and software. Sells directly to consumers (D2C) and operates physical experience centers. Future monetization focuses on software subscriptions, battery-as-a-service, and exports.',
    financialSummary: {
      years: ['FY22', 'FY23', 'FY24'],
      revenue: [373, 2630, 5009],
      profit: [-784, -1472, -1584],
      ebitda: [-620, -1120, -1250]
    },
    strengths: [
      'Market leader in electric two-wheelers with >35% share.',
      'In-house battery cell development and scale factory advantages.',
      'Favorable government policies and EV subsidies.'
    ],
    risks: [
      'High dependence on FAME-II and state government subsidies.',
      'Product safety issues (battery fires, software bugs).',
      'Execution risks in expanding capacity and launching electric cars.'
    ],
    swot: {
      strengths: ['Vertically integrated R&D', 'First-mover advantage in scale EV', 'Strong D2C channel'],
      weaknesses: ['Product reliability issues', 'Heavy dependence on imported cell materials', 'Capital intensive model'],
      opportunities: ['Battery cell export market', 'Launching EV three-wheelers and passenger cars', 'Gigafactory expansion'],
      threats: ['Decline in government subsidies', 'Entry of established legacy manufacturers (TVS, Bajaj)', 'Global lithium price volatility']
    }
  },
  {
    id: 'bajaj-housing',
    name: 'Bajaj Housing Finance',
    ticker: 'BAJAJHFL',
    sector: 'Finance & Housing HFC',
    status: 'Listed',
    priceBand: { min: 66, max: 70 },
    issueSize: 6560,
    lotSize: 214,
    openDate: '2026-06-08',
    closeDate: '2026-06-11',
    allotmentDate: '2026-06-12',
    refundDate: '2026-06-13',
    listingDate: '2026-06-16',
    aiScore: 94,
    aiRecommendation: 'Strong Buy',
    gmp: 110,
    overview: 'Bajaj Housing Finance is a non-deposit taking housing finance company registered with the National Housing Bank. Part of the prestigious Bajaj Group, it offers home loans, loans against property, and developer finance to customers across India.',
    businessModel: 'Interest spread income from long-term home and property loans. Minimizes cost of funds through high-quality credit rating (AAA) and leverages Bajaj Finance\'s massive cross-sell database.',
    financialSummary: {
      years: ['FY22', 'FY23', 'FY24'],
      revenue: [3767, 5665, 7618],
      profit: [710, 1258, 1731],
      ebitda: [950, 1680, 2410]
    },
    strengths: [
      'Strong parentage and AAA credit rating, leading to low borrowing costs.',
      'Exceptional asset quality with GNPA under 0.3%.',
      'Robust cross-selling integration with Bajaj Finance.'
    ],
    risks: [
      'Intense competition in the prime home loan segment.',
      'Interest rate fluctuation risks affecting margins.',
      'Potential stress in developer finance portfolio.'
    ],
    swot: {
      strengths: ['Lowest GNPA in HFC sector', 'AAA credit rating stability', 'Advanced digital loan processing'],
      weaknesses: ['Low yields in prime segment', 'Geographic concentration in western states', 'Higher developer loan exposure'],
      opportunities: ['Affordable housing sector expansion', 'Co-lending partnerships', 'Digital self-service channels'],
      threats: ['Sudden policy rate hikes by RBI', 'Slowing real estate demand', 'Asset-liability mismatch under high inflation']
    }
  },
  {
    id: 'ola-cabs',
    name: 'Ani Technologies (Ola Cabs)',
    ticker: 'OLACABS',
    sector: 'Technology & Ride Hailing',
    status: 'Draft',
    priceBand: { min: 250, max: 275 },
    issueSize: 4500,
    lotSize: 55,
    openDate: '2026-09-10',
    closeDate: '2026-09-13',
    allotmentDate: '2026-09-14',
    refundDate: '2026-09-15',
    listingDate: '2026-09-18',
    aiScore: 68,
    aiRecommendation: 'Hold',
    gmp: 5,
    overview: 'Ani Technologies, operating as Ola Cabs, is India\'s largest ride-hailing company with operations in over 200 cities. It offers a range of services including app-based taxi bookings, auto-rickshaw hire, and outstation travels.',
    businessModel: 'Platform aggregator model collecting commissions (20-25%) from driver earnings. Generates secondary revenue from subscription passes, corporate travel programs, and consumer lending.',
    financialSummary: {
      years: ['FY22', 'FY23', 'FY24'],
      revenue: [1973, 2790, 3120],
      profit: [-1520, -772, -350],
      ebitda: [-890, -220, 110]
    },
    strengths: [
      'Massive scale and brand awareness across Tier 1 & 2 cities.',
      'Integrated auto and bike segments providing stable margins.',
      'Turnaround in EBITDA, approaching company-level profit.'
    ],
    risks: [
      'Regulatory cap on commission models and surge pricing.',
      'High driver attrition rates and labor union strikes.',
      'Competition from Uber and fast-growing local alternatives like Namma Yatri.'
    ],
    swot: {
      strengths: ['High driver network effect', 'Strong digital platform security', 'Diverse fleet type (Auto, Bike, Prime)'],
      weaknesses: ['Vulnerable supply control', 'Low customer loyalty in commodity segment', 'High legal and regulatory litigation fees'],
      opportunities: ['Transitioning corporate fleet to EV', 'Deep integration with Ola Electric', 'Airport kiosk travel monetization'],
      threats: ['Strict government regulation on driver safety and wages', 'Zero-commission platforms', 'Economic slowdowns affecting discretionary travel']
    }
  }
];

export const mockTransactions: Transaction[] = [
  {
    id: 'pay_9F2G7H8',
    userName: 'Rahul Kumar',
    userEmail: 'rahul@example.com',
    amount: 499,
    date: '2026-07-15 13:04',
    status: 'Success'
  },
  {
    id: 'pay_1A2B3C4',
    userName: 'Ashwani Vishwakarma',
    userEmail: 'ashwani@example.com',
    amount: 499,
    date: '2026-07-14 18:22',
    status: 'Success'
  },
  {
    id: 'pay_5D6E7F8',
    userName: 'Pooja Sharma',
    userEmail: 'pooja@example.com',
    amount: 499,
    date: '2026-07-12 11:15',
    status: 'Failed'
  },
  {
    id: 'pay_9A0B1C2',
    userName: 'Vikram Singh',
    userEmail: 'vikram@example.com',
    amount: 4999,
    date: '2026-07-10 16:45',
    status: 'Success'
  },
  {
    id: 'pay_3X4Y5Z6',
    userName: 'Amit Patel',
    userEmail: 'amit@example.com',
    amount: 499,
    date: '2026-07-08 09:30',
    status: 'Refunded'
  }
];
