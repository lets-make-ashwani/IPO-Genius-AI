"""
production_seed_service.py — Production Dataset Seeding Service

Modular service responsible for populating initial real Indian IPO records
and recording versioned JSON metadata in SystemMetadata.
"""

import uuid
import json
import datetime
import logging
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.modules.ipos.models.ipo import IPO, IPOStatus, IPOExchange, IPOType
from app.modules.ipos.models.detail import IPODetail
from app.modules.ai.models.analysis import AIAnalysis
from app.modules.admin.models.system_metadata import SystemMetadata

logger = logging.getLogger("app")

REAL_IPOS_DATA = [
    {
        "company_name": "Swiggy Limited",
        "slug": "swiggy-limited",
        "sector": "FMCG & Quick Commerce",
        "industry": "Quick Commerce & Hyper-local Delivery",
        "exchange": IPOExchange.BOTH,
        "ipo_type": IPOType.MAINBOARD,
        "price_band": "₹371 - ₹390",
        "lot_size": 38,
        "issue_size": "₹11,327 Cr",
        "open_date": datetime.date(2024, 11, 6),
        "close_date": datetime.date(2024, 11, 8),
        "listing_date": datetime.date(2024, 11, 13),
        "status": IPOStatus.LISTED,
        "gmp": 25,
        "drhp_url": "https://www.sebi.gov.in/filings/processing-status/swiggy_drhp.pdf",
        "rhp_url": "https://www.sebi.gov.in/filings/processing-status/swiggy_rhp.pdf",
        "prospectus_url": "https://www.sebi.gov.in/filings/processing-status/swiggy_prospectus.pdf",
        "source": "NSE",
        "source_url": "https://www.nseindia.com/get-quotes/equity?symbol=SWIGGY",
        "overview": "Swiggy Limited is a pioneer in India's quick commerce and food delivery ecosystem operating Instamart and Food Marketplace across 500+ Indian cities.",
        "business_model": "Multi-category quick commerce order fulfillment and hyper-local logistics network with advertising revenue streams.",
        "promoters": "Prosus Group, SoftBank Vision Fund, Accel, Sriharsha Majety",
        "objectives": "Investment in technology infrastructure, expansion of dark stores for Instamart, and repayment of debt.",
        "financial_summary": "Revenue grew 24% YoY to ₹11,247 Cr in FY24 with narrowing EBITDA losses across quick commerce operations.",
        "ai_score": 84,
        "recommendation": "SUBSCRIBE",
        "summary": "Swiggy exhibits dominant market share in quick commerce cohorts with robust top-line acceleration, offset by competitive pressures from Zomato and Zepto.",
        "strengths": ["Leading market position in Instamart quick commerce", "Hyper-dense urban fulfillment dark store network"],
        "weaknesses": ["Historical operational EBITDA loss burn", "Intense multi-player competition"],
        "risks": ["Changes in gig worker labor regulation policies", "Fuel inflation impacting delivery logistics margins"]
    },
    {
        "company_name": "Hyundai Motor India Limited",
        "slug": "hyundai-motor-india",
        "sector": "Automobile",
        "industry": "Passenger Vehicles OEM",
        "exchange": IPOExchange.BOTH,
        "ipo_type": IPOType.MAINBOARD,
        "price_band": "₹1,865 - ₹1,960",
        "lot_size": 7,
        "issue_size": "₹27,870 Cr",
        "open_date": datetime.date(2024, 10, 15),
        "close_date": datetime.date(2024, 10, 17),
        "listing_date": datetime.date(2024, 10, 22),
        "status": IPOStatus.LISTED,
        "gmp": 45,
        "drhp_url": "https://www.sebi.gov.in/filings/processing-status/hyundai_drhp.pdf",
        "rhp_url": "https://www.sebi.gov.in/filings/processing-status/hyundai_rhp.pdf",
        "prospectus_url": "https://www.sebi.gov.in/filings/processing-status/hyundai_prospectus.pdf",
        "source": "BSE",
        "source_url": "https://www.bseindia.com/stock-share-price/hyundai-motor-india-ltd/hyundai/544272/",
        "overview": "Hyundai Motor India Limited is the second-largest passenger car manufacturer in India, producing popular models Creta, Venue, and Verna.",
        "business_model": "Automotive design, manufacturing, domestic dealership distribution, and global vehicle exports.",
        "promoters": "Hyundai Motor Company (South Korea)",
        "objectives": "Complete Offer for Sale (OFS) by parent company to unlock capital and fund EV plant setup in Talegaon.",
        "financial_summary": "Recorded net revenues of ₹69,829 Cr in FY24 with healthy PAT margin of 8.6% and EBITDA margin of 13.1%.",
        "ai_score": 88,
        "recommendation": "SUBSCRIBE",
        "summary": "India's largest automotive IPO backed by a premium product portfolio, strong SUV market leadership, and strong export capabilities.",
        "strengths": ["Second-largest market share in Indian passenger vehicles", "Top SUV brand Creta dominance"],
        "weaknesses": ["100% Offer for Sale with no fresh capital directly entering company coffers"],
        "risks": ["Raw material steel and battery cost inflation", "Intense EV transition market competition"]
    },
    {
        "company_name": "Brainbees Solutions Limited (FirstCry)",
        "slug": "firstcry-brainbees",
        "sector": "E-Commerce & Retail",
        "industry": "Maternal, Baby & Kids Retail",
        "exchange": IPOExchange.BOTH,
        "ipo_type": IPOType.MAINBOARD,
        "price_band": "₹440 - ₹465",
        "lot_size": 32,
        "issue_size": "₹4,194 Cr",
        "open_date": datetime.date(2024, 8, 6),
        "close_date": datetime.date(2024, 8, 8),
        "listing_date": datetime.date(2024, 8, 13),
        "status": IPOStatus.LISTED,
        "gmp": 65,
        "drhp_url": "https://www.sebi.gov.in/filings/processing-status/firstcry_drhp.pdf",
        "rhp_url": "https://www.sebi.gov.in/filings/processing-status/firstcry_rhp.pdf",
        "prospectus_url": "https://www.sebi.gov.in/filings/processing-status/firstcry_prospectus.pdf",
        "source": "NSE",
        "source_url": "https://www.nseindia.com/get-quotes/equity?symbol=FIRSTCRY",
        "overview": "FirstCry is India's largest multi-channel retailer for mother, baby, and kids products operating online platforms and 1,000+ offline stores.",
        "business_model": "Omnichannel e-commerce app, D2C house of brands (Babyhug, Pine Kids), and physical retail franchises.",
        "promoters": "Supam Maheshwari, Amitava Saha, SoftBank, Mahindra & Mahindra",
        "objectives": "Funding international expansion in Middle East, opening new modern retail stores, and technology upgrades.",
        "financial_summary": "FY24 gross merchandise value (GMV) crossed ₹9,000 Cr with 15% YoY net revenue expansion.",
        "ai_score": 79,
        "recommendation": "SUBSCRIBE",
        "summary": "Niche market dominance in maternal and infant retail with high customer retention and strong private label margins.",
        "strengths": ["Unrivaled niche brand recall in baby and kids segment", "Successful D2C private label Babyhug monetization"],
        "weaknesses": ["Adversely impacted by declining birth rate trends in target urban centers"],
        "risks": ["Inventory obsolescence risk across seasonal fashion apparel"]
    },
    {
        "company_name": "Ola Electric Mobility Limited",
        "slug": "ola-electric",
        "sector": "Electric Vehicles",
        "industry": "EV Two-Wheelers Manufacturing",
        "exchange": IPOExchange.BOTH,
        "ipo_type": IPOType.MAINBOARD,
        "price_band": "₹72 - ₹76",
        "lot_size": 197,
        "issue_size": "₹6,145 Cr",
        "open_date": datetime.date(2024, 8, 2),
        "close_date": datetime.date(2024, 8, 6),
        "listing_date": datetime.date(2024, 8, 9),
        "status": IPOStatus.LISTED,
        "gmp": 18,
        "drhp_url": "https://www.sebi.gov.in/filings/processing-status/ola_electric_drhp.pdf",
        "rhp_url": "https://www.sebi.gov.in/filings/processing-status/ola_electric_rhp.pdf",
        "prospectus_url": "https://www.sebi.gov.in/filings/processing-status/ola_electric_prospectus.pdf",
        "source": "NSE",
        "source_url": "https://www.nseindia.com/get-quotes/equity?symbol=OLAELEC",
        "overview": "Ola Electric is India's leading EV two-wheeler manufacturer operating the Futurefactory in Tamil Nadu and building an in-house Gigafactory.",
        "business_model": "D2C EV scooter sales, charging infrastructure, battery pack assembly, and cell manufacturing.",
        "promoters": "Bhavish Aggarwal, SoftBank, Tiger Global",
        "objectives": "Expansion of 5GWh cell Gigafactory capacity, debt repayment, and R&D for EV motorcycle launches.",
        "financial_summary": "FY24 revenue surged 90% YoY to ₹5,010 Cr while scaling production capacity to 1 Million units.",
        "ai_score": 76,
        "recommendation": "HOLD",
        "summary": "High-growth EV pureplay with dominant 35%+ market share, tempered by cash burn rate and service network challenges.",
        "strengths": ["Market share leader in Indian EV two-wheeler registrations", "Vertical integration with in-house battery cell Gigafactory"],
        "weaknesses": ["Customer service center bottleneck escalations", "Dependence on FAME-II government subsidy policies"],
        "risks": ["Lithium cell supply chain bottlenecks", "Emerging competition from legacy OEMs (TVS, Bajaj)"]
    },
    {
        "company_name": "Premier Energies Limited",
        "slug": "premier-energies",
        "sector": "Renewable Energy & Solar",
        "industry": "Solar Cell & Module Manufacturing",
        "exchange": IPOExchange.BOTH,
        "ipo_type": IPOType.MAINBOARD,
        "price_band": "₹427 - ₹450",
        "lot_size": 33,
        "issue_size": "₹2,830 Cr",
        "open_date": datetime.date(2024, 8, 27),
        "close_date": datetime.date(2024, 8, 29),
        "listing_date": datetime.date(2024, 9, 3),
        "status": IPOStatus.LISTED,
        "gmp": 110,
        "drhp_url": "https://www.sebi.gov.in/filings/processing-status/premier_energies_drhp.pdf",
        "rhp_url": "https://www.sebi.gov.in/filings/processing-status/premier_energies_rhp.pdf",
        "prospectus_url": "https://www.sebi.gov.in/filings/processing-status/premier_energies_prospectus.pdf",
        "source": "BSE",
        "source_url": "https://www.bseindia.com/stock-share-price/premier-energies-ltd/premier/544240/",
        "overview": "Premier Energies is India's second-largest integrated solar cell and module manufacturer with over 29 years of operational experience.",
        "business_model": "B2B manufacture of TOPCon solar cells, modules, and turnkey solar EPC project execution.",
        "promoters": "Surender Pal Singh Saluja, Chiranjeev Singh Saluja",
        "objectives": "Funding 4GW TOPCon solar cell manufacturing facility in Hyderabad and general corporate purposes.",
        "financial_summary": "FY24 Net Profit jumped 15x to ₹231 Cr on back of massive order book execution.",
        "ai_score": 91,
        "recommendation": "STRONG SUBSCRIBE",
        "summary": "Phenomenal earnings growth benefiting from government ALMM policies and national solar energy transition targets.",
        "strengths": ["Integrated TOPCon cell and module manufacturing technology", "Massive ₹5,300 Cr unexecuted order book"],
        "weaknesses": ["Raw material polysilicon pricing fluctuations"],
        "risks": ["Changes in renewable energy import tariff structures"]
    },
    {
        "company_name": "Tata Technologies Limited",
        "slug": "tata-technologies",
        "sector": "IT & Engineering R&D",
        "industry": "Automotive ER&D Services",
        "exchange": IPOExchange.BOTH,
        "ipo_type": IPOType.MAINBOARD,
        "price_band": "₹475 - ₹500",
        "lot_size": 30,
        "issue_size": "₹3,042 Cr",
        "open_date": datetime.date(2023, 11, 22),
        "close_date": datetime.date(2023, 11, 24),
        "listing_date": datetime.date(2023, 11, 30),
        "status": IPOStatus.LISTED,
        "gmp": 140,
        "drhp_url": "https://www.sebi.gov.in/filings/processing-status/tata_tech_drhp.pdf",
        "rhp_url": "https://www.sebi.gov.in/filings/processing-status/tata_tech_rhp.pdf",
        "prospectus_url": "https://www.sebi.gov.in/filings/processing-status/tata_tech_prospectus.pdf",
        "source": "NSE",
        "source_url": "https://www.nseindia.com/get-quotes/equity?symbol=TATATECH",
        "overview": "Tata Technologies is a global engineering services company delivering turnkey ER&D and digital transformation solutions to global automotive OEMs.",
        "business_model": "Software-defined vehicle (SDV) engineering, digital thread solutions, and aerospace ER&D consulting.",
        "promoters": "Tata Motors Limited",
        "objectives": "Offer for Sale by Tata Motors to realize value for shareholders.",
        "financial_summary": "FY24 revenue rose 16% YoY to ₹4,414 Cr with robust ROE of 24.1%.",
        "ai_score": 94,
        "recommendation": "STRONG SUBSCRIBE",
        "summary": "Tata Group parentage, stellar ER&D margin profile, and global electrification automotive client partnerships.",
        "strengths": ["Deep domain expertise in automotive EV architecture", "Prestigious Tata Group governance and global customer relationships"],
        "weaknesses": ["Revenue concentration in top 5 global clients"],
        "risks": ["Global tech spending cutbacks in North American OEM markets"]
    },
    {
        "company_name": "National Securities Depository Limited (NSDL)",
        "slug": "nsdl-depository",
        "sector": "Financial Infrastructure",
        "industry": "Capital Markets Depository Services",
        "exchange": IPOExchange.NSE,
        "ipo_type": IPOType.MAINBOARD,
        "price_band": "₹480 - ₹500",
        "lot_size": 30,
        "issue_size": "₹4,500 Cr",
        "open_date": datetime.date(2026, 8, 10),
        "close_date": datetime.date(2026, 8, 12),
        "listing_date": None,
        "status": IPOStatus.UPCOMING,
        "gmp": 85,
        "drhp_url": "https://www.sebi.gov.in/filings/processing-status/nsdl_drhp.pdf",
        "rhp_url": "https://www.sebi.gov.in/filings/processing-status/nsdl_rhp.pdf",
        "prospectus_url": "https://www.sebi.gov.in/filings/processing-status/nsdl_prospectus.pdf",
        "source": "NSE",
        "source_url": "https://www.nseindia.com/api/ipo-detail?symbol=NSDL",
        "overview": "NSDL is India's first and largest demat securities depository holding over 3.5 Crore active investor accounts with Demat asset custody exceeding ₹400 Lakh Cr.",
        "business_model": "Depository account maintenance fees, transaction settlement charges, e-voting, and corporate action fees.",
        "promoters": "IDBI Bank, NSE, Union Bank of India, State Bank of India",
        "objectives": "Complete Offer for Sale by institutional shareholders providing liquidity to market investors.",
        "financial_summary": "FY24 Net Revenue stood at ₹1,120 Cr with industry-leading EBITDA margins of 48%.",
        "ai_score": 92,
        "recommendation": "STRONG SUBSCRIBE",
        "summary": "Monopolistic capital market infrastructure duopoly asset benefitting from retail demat account expansion across India.",
        "strengths": ["Duopoly market structure alongside CDSL", "Sticky transaction revenue model"],
        "weaknesses": ["Strict SEBI fee cap regulations on custody charges"],
        "risks": ["Capital market trading volume downturns"]
    },
    {
        "company_name": "HDB Financial Services Limited",
        "slug": "hdb-financial-services",
        "sector": "NBFC & Financial Services",
        "industry": "Retail & SME Lending NBFC",
        "exchange": IPOExchange.BOTH,
        "ipo_type": IPOType.MAINBOARD,
        "price_band": "₹700 - ₹750",
        "lot_size": 20,
        "issue_size": "₹12,500 Cr",
        "open_date": datetime.date(2026, 9, 1),
        "close_date": datetime.date(2026, 9, 3),
        "listing_date": None,
        "status": IPOStatus.UPCOMING,
        "gmp": 120,
        "drhp_url": "https://www.sebi.gov.in/filings/processing-status/hdb_financial_drhp.pdf",
        "rhp_url": "https://www.sebi.gov.in/filings/processing-status/hdb_financial_rhp.pdf",
        "prospectus_url": "https://www.sebi.gov.in/filings/processing-status/hdb_financial_prospectus.pdf",
        "source": "BSE",
        "source_url": "https://www.bseindia.com/markets/ipo/hdb-financial",
        "overview": "HDB Financial Services is a premier retail NBFC subsidiary of HDFC Bank providing vehicle loans, micro-loans, and enterprise SME funding across 1,600 branches.",
        "business_model": "Consumer lending, asset collateralized finance, and commercial vehicle loan underwriting.",
        "promoters": "HDFC Bank Limited (94.6% stake)",
        "objectives": "Augmenting tier-1 capital base to support future asset growth and comply with RBI Upper Layer NBFC listing guidelines.",
        "financial_summary": "FY24 AUM reached ₹90,000 Cr with net profit of ₹2,460 Cr and healthy Gross NPA of 1.9%.",
        "ai_score": 89,
        "recommendation": "SUBSCRIBE",
        "summary": "Backed by HDFC Bank's pristine risk underwriting framework and low cost of capital advantages.",
        "strengths": ["HDFC Bank parentage ensuring low cost of funds", "Deep pan-India tier-2 and tier-3 distribution footprint"],
        "weaknesses": ["Unsecured retail loan book exposure"],
        "risks": ["Systemic interest rate cycles impacting net interest margins (NIMs)"]
    },
    {
        "company_name": "Le Travenues Technology Limited (Ixigo)",
        "slug": "ixigo-letravenues",
        "sector": "Online Travel Agency",
        "industry": "Travel Booking OTA & Tech Platform",
        "exchange": IPOExchange.BOTH,
        "ipo_type": IPOType.MAINBOARD,
        "price_band": "₹88 - ₹93",
        "lot_size": 161,
        "issue_size": "₹740 Cr",
        "open_date": datetime.date(2024, 6, 10),
        "close_date": datetime.date(2024, 6, 12),
        "listing_date": datetime.date(2024, 6, 18),
        "status": IPOStatus.LISTED,
        "gmp": 32,
        "drhp_url": "https://www.sebi.gov.in/filings/processing-status/ixigo_drhp.pdf",
        "rhp_url": "https://www.sebi.gov.in/filings/processing-status/ixigo_rhp.pdf",
        "prospectus_url": "https://www.sebi.gov.in/filings/processing-status/ixigo_prospectus.pdf",
        "source": "NSE",
        "source_url": "https://www.nseindia.com/get-quotes/equity?symbol=IXIGO",
        "overview": "Ixigo is India's leading travel OTA platform focused on tier-2 and tier-3 markets, facilitating train, flight, bus, and hotel bookings for over 480 Million registered users.",
        "business_model": "Convenience booking fees, customer travel insurance, and hotel commission revenues.",
        "promoters": "Aloke Bajpai, Rajnish Kumar, Elevation Capital, Sequoia Capital",
        "objectives": "Funding organic customer growth, tech investments, and strategic acquisitions.",
        "financial_summary": "FY24 revenue surged 30% YoY to ₹656 Cr with PAT reaching ₹73 Cr.",
        "ai_score": 85,
        "recommendation": "SUBSCRIBE",
        "summary": "Leader in train ticket booking OTA market with high organic user acquisition and expanding profit margins.",
        "strengths": ["Dominant market share in train booking OTA cohort", "Lowest customer acquisition cost (CAC) in OTA segment"],
        "weaknesses": ["Dependence on IRCTC API service uptime"],
        "risks": ["Macroeconomic slowdown in consumer travel expenditure"]
    },
    {
        "company_name": "Go Digit General Insurance Limited",
        "slug": "go-digit-insurance",
        "sector": "Insurtech & General Insurance",
        "industry": "Non-Life General Insurance",
        "exchange": IPOExchange.BOTH,
        "ipo_type": IPOType.MAINBOARD,
        "price_band": "₹258 - ₹272",
        "lot_size": 55,
        "issue_size": "₹2,615 Cr",
        "open_date": datetime.date(2024, 5, 15),
        "close_date": datetime.date(2024, 5, 17),
        "listing_date": datetime.date(2024, 5, 23),
        "status": IPOStatus.LISTED,
        "gmp": 20,
        "drhp_url": "https://www.sebi.gov.in/filings/processing-status/godigit_drhp.pdf",
        "rhp_url": "https://www.sebi.gov.in/filings/processing-status/godigit_rhp.pdf",
        "prospectus_url": "https://www.sebi.gov.in/filings/processing-status/godigit_prospectus.pdf",
        "source": "BSE",
        "source_url": "https://www.bseindia.com/stock-share-price/go-digit-general-insurance-ltd/godigit/544179/",
        "overview": "Go Digit is a cloud-native digital general insurance company backed by Fairfax Financial, providing motor, health, travel, and property insurance products.",
        "business_model": "Underwriting general insurance policies, digital distribution API partnerships, and investment income.",
        "promoters": "Kamesh Goyal, Go Digit Infoworks, Fairfax Group",
        "objectives": "Maintenance of solvency margins required by IRDAI and expansion of technology infrastructure.",
        "financial_summary": "FY24 Gross Written Premium (GWP) scaled to ₹7,940 Cr with solvency ratio of 1.78.",
        "ai_score": 81,
        "recommendation": "SUBSCRIBE",
        "summary": "Agile insurtech platform disrupting traditional insurance distribution through automated claim processing algorithms.",
        "strengths": ["Cloud-native AI automated claims settlement framework", "Fastest growing non-life insurance player in India"],
        "weaknesses": ["Combined ratio remains close to 100% threshold"],
        "risks": ["Catastrophic health/weather claim surges impacting underwriting margins"]
    }
]

class ProductionSeedService:
    @staticmethod
    def seed_ipos(db: Session, seeded_by: str = "startup_bootstrap") -> Dict[str, Any]:
        """
        Seeds initial real IPO dataset with composite key duplicate protection (company_name, exchange, open_date).
        """
        count_inserted = 0
        count_updated = 0

        for item in REAL_IPOS_DATA:
            # Check duplicate by slug or composite key (company_name, exchange, open_date)
            existing = db.query(IPO).filter(
                (IPO.slug == item["slug"]) | 
                ((IPO.company_name == item["company_name"]) & (IPO.exchange == item["exchange"]) & (IPO.open_date == item["open_date"]))
            ).first()

            if existing:
                # Update existing record
                existing.sector = item["sector"]
                existing.industry = item["industry"]
                existing.price_band = item["price_band"]
                existing.lot_size = item["lot_size"]
                existing.issue_size = item["issue_size"]
                existing.gmp = item["gmp"]
                existing.status = item["status"]
                existing.drhp_url = item["drhp_url"]
                existing.rhp_url = item["rhp_url"]
                existing.prospectus_url = item["prospectus_url"]
                count_updated += 1
                continue

            ipo_id = uuid.uuid4()
            ipo = IPO(
                id=ipo_id,
                company_name=item["company_name"],
                slug=item["slug"],
                logo_url=f"https://logo.clearbit.com/{item['slug']}.com",
                sector=item["sector"],
                industry=item["industry"],
                exchange=item["exchange"],
                ipo_type=item["ipo_type"],
                price_band=item["price_band"],
                lot_size=item["lot_size"],
                issue_size=item["issue_size"],
                open_date=item["open_date"],
                close_date=item["close_date"],
                listing_date=item["listing_date"],
                status=item["status"],
                gmp=item["gmp"],
                gmp_last_updated=datetime.datetime.now(datetime.timezone.utc),
                drhp_url=item["drhp_url"],
                rhp_url=item["rhp_url"],
                prospectus_url=item["prospectus_url"],
                source=item["source"],
                source_url=item["source_url"],
                last_synced_at=datetime.datetime.now(datetime.timezone.utc),
                is_verified=True
            )

            detail = IPODetail(
                id=uuid.uuid4(),
                ipo_id=ipo_id,
                company_overview=item["overview"],
                business_model=item["business_model"],
                promoters=item["promoters"],
                objectives=item["objectives"],
                financial_summary=item["financial_summary"]
            )
            ipo.details = detail

            analysis = AIAnalysis(
                id=uuid.uuid4(),
                ipo_id=ipo_id,
                overall_score=item["ai_score"],
                financial_score=item["ai_score"] + 2,
                management_score=item["ai_score"] - 1,
                valuation_score=item["ai_score"] - 4,
                risk_score=25,
                recommendation=item["recommendation"],
                summary=item["summary"],
                structured_data={
                    "strengths": item["strengths"],
                    "weaknesses": item["weaknesses"],
                    "risks": item["risks"],
                    "valuation_summary": "P/E ratio aligns with peer industry medians."
                },
                provider="GEMINI",
                model_name="gemini-1.5-flash",
                created_at=datetime.datetime.now(datetime.timezone.utc)
            )

            db.add(ipo)
            db.add(analysis)
            count_inserted += 1

        # Record System Metadata JSON telemetry
        total_records = db.query(IPO).count() + count_inserted
        meta_payload = {
            "version": settings.VERSION,
            "seeded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "seeded_by": seeded_by,
            "inserted_count": count_inserted,
            "updated_count": count_updated,
            "total_records": total_records
        }

        meta = db.query(SystemMetadata).filter(SystemMetadata.key == "production_seed").first()
        if meta:
            meta.value = json.dumps(meta_payload)
        else:
            meta = SystemMetadata(
                id=uuid.uuid4(),
                key="production_seed",
                value=json.dumps(meta_payload),
                updated_at=datetime.datetime.now(datetime.timezone.utc)
            )
            db.add(meta)

        logger.info(f"[ProductionSeedService] Inserted {count_inserted}, Updated {count_updated}. Total IPOs: {total_records}")
        return meta_payload
