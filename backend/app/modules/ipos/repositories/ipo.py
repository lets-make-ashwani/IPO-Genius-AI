from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc
from typing import Optional, List, Tuple
import uuid
from app.modules.ipos.models.ipo import IPO, IPOStatus, IPOType
from app.modules.ipos.models.detail import IPODetail

class IPORepository:
    def get_by_id(self, db: Session, ipo_id: uuid.UUID) -> Optional[IPO]:
        return (
            db.query(IPO)
            .options(joinedload(IPO.details))
            .filter(IPO.id == ipo_id)
            .first()
        )

    def get_by_slug(self, db: Session, slug: str) -> Optional[IPO]:
        return (
            db.query(IPO)
            .options(joinedload(IPO.details))
            .filter(IPO.slug == slug)
            .first()
        )

    def get_ipos(
        self,
        db: Session,
        status: Optional[IPOStatus] = None,
        ipo_type: Optional[IPOType] = None,
        exchange: Optional[str] = None,
        sector: Optional[str] = None,
        industry: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = "open_date",
        sort_order: Optional[str] = "desc",
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[IPO], int]:
        query = db.query(IPO).options(joinedload(IPO.details))

        if status is not None:
            query = query.filter(IPO.status == (status.value if hasattr(status, 'value') else status))
        
        if ipo_type is not None:
            query = query.filter(IPO.ipo_type == (ipo_type.value if hasattr(ipo_type, 'value') else ipo_type))

        if exchange is not None and exchange.strip() != "":
            query = query.filter(IPO.exchange == exchange.strip().upper())

        if sector is not None and sector.strip() != "":
            query = query.filter(IPO.sector.ilike(f"%{sector.strip()}%"))

        if industry is not None and industry.strip() != "":
            query = query.filter(IPO.industry.ilike(f"%{industry.strip()}%"))

        if search is not None and search.strip() != "":
            search_pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    IPO.company_name.ilike(search_pattern),
                    IPO.sector.ilike(search_pattern),
                    IPO.industry.ilike(search_pattern)
                )
            )

        total = query.count()

        # Dynamic Sorting
        from sqlalchemy import asc, desc
        sort_column = getattr(IPO, sort_by, IPO.open_date) if sort_by in ["open_date", "close_date", "gmp", "company_name"] else IPO.open_date
        order_func = asc if (sort_order and sort_order.lower() == "asc") else desc

        results = (
            query.order_by(order_func(sort_column))
            .offset(offset)
            .limit(limit)
            .all()
        )

        return results, total


    def create(self, db: Session, ipo_data, slug: str) -> IPO:
        # Validate unique company name
        existing_name = db.query(IPO).filter(IPO.company_name == ipo_data.company_name).first()
        if existing_name:
            from app.shared.exceptions import AppException
            from fastapi import status
            raise AppException("IPO with this company name already exists", status_code=status.HTTP_400_BAD_REQUEST)

        # Validate unique slug
        existing_slug = db.query(IPO).filter(IPO.slug == slug).first()
        if existing_slug:
            from app.shared.exceptions import AppException
            from fastapi import status
            raise AppException("IPO with this slug already exists", status_code=status.HTTP_400_BAD_REQUEST)

        ipo = IPO(
            id=uuid.uuid4(),
            company_name=ipo_data.company_name,
            slug=slug,
            logo_url=ipo_data.logo_url,
            sector=ipo_data.sector,
            industry=ipo_data.industry,
            exchange=ipo_data.exchange,
            ipo_type=ipo_data.ipo_type,
            price_band=ipo_data.price_band,
            lot_size=ipo_data.lot_size,
            issue_size=ipo_data.issue_size,
            open_date=ipo_data.open_date,
            close_date=ipo_data.close_date,
            listing_date=ipo_data.listing_date,
            status=ipo_data.status,
            gmp=ipo_data.gmp,
            gmp_last_updated=ipo_data.gmp_last_updated,
            total_subscription=getattr(ipo_data, "total_subscription", 0.0) or 0.0,
            drhp_url=ipo_data.drhp_url,
            rhp_url=ipo_data.rhp_url,
            prospectus_url=ipo_data.prospectus_url,
            source=ipo_data.source,
            source_url=ipo_data.source_url,
            is_verified=ipo_data.is_verified
        )

        if ipo_data.details:
            details = IPODetail(
                id=uuid.uuid4(),
                company_overview=ipo_data.details.company_overview,
                business_model=ipo_data.details.business_model,
                promoters=ipo_data.details.promoters,
                objectives=ipo_data.details.objectives,
                financial_summary=ipo_data.details.financial_summary
            )
            ipo.details = details

        db.add(ipo)
        db.commit()
        db.refresh(ipo)
        return ipo

    def update(self, db: Session, ipo: IPO, ipo_data) -> IPO:
        from app.shared.exceptions import AppException
        from fastapi import status

        # Validate unique company name if changing
        if ipo_data.company_name is not None and ipo_data.company_name != ipo.company_name:
            existing_name = db.query(IPO).filter(IPO.company_name == ipo_data.company_name).first()
            if existing_name:
                raise AppException("IPO with this company name already exists", status_code=status.HTTP_400_BAD_REQUEST)
            ipo.company_name = ipo_data.company_name

        # Validate unique slug if changing
        if ipo_data.slug is not None and ipo_data.slug != ipo.slug:
            existing_slug = db.query(IPO).filter(IPO.slug == ipo_data.slug).first()
            if existing_slug:
                raise AppException("IPO with this slug already exists", status_code=status.HTTP_400_BAD_REQUEST)
            ipo.slug = ipo_data.slug

        if ipo_data.logo_url is not None:
            ipo.logo_url = ipo_data.logo_url
        if ipo_data.sector is not None:
            ipo.sector = ipo_data.sector
        if ipo_data.industry is not None:
            ipo.industry = ipo_data.industry
        if ipo_data.exchange is not None:
            ipo.exchange = ipo_data.exchange
        if ipo_data.ipo_type is not None:
            ipo.ipo_type = ipo_data.ipo_type
        if ipo_data.price_band is not None:
            ipo.price_band = ipo_data.price_band
        if ipo_data.lot_size is not None:
            ipo.lot_size = ipo_data.lot_size
        if ipo_data.issue_size is not None:
            ipo.issue_size = ipo_data.issue_size
        if ipo_data.open_date is not None:
            ipo.open_date = ipo_data.open_date
        if ipo_data.close_date is not None:
            ipo.close_date = ipo_data.close_date
        if ipo_data.listing_date is not None:
            ipo.listing_date = ipo_data.listing_date
        if ipo_data.status is not None:
            ipo.status = ipo_data.status
        if ipo_data.gmp is not None:
            ipo.gmp = ipo_data.gmp
        if ipo_data.gmp_last_updated is not None:
            ipo.gmp_last_updated = ipo_data.gmp_last_updated
        if getattr(ipo_data, "total_subscription", None) is not None:
            ipo.total_subscription = ipo_data.total_subscription
        if ipo_data.drhp_url is not None:
            ipo.drhp_url = ipo_data.drhp_url
        if ipo_data.rhp_url is not None:
            ipo.rhp_url = ipo_data.rhp_url
        if ipo_data.prospectus_url is not None:
            ipo.prospectus_url = ipo_data.prospectus_url
        if ipo_data.source is not None:
            ipo.source = ipo_data.source
        if ipo_data.source_url is not None:
            ipo.source_url = ipo_data.source_url
        if ipo_data.is_verified is not None:
            ipo.is_verified = ipo_data.is_verified

        if ipo_data.details:
            if not ipo.details:
                ipo.details = IPODetail(id=uuid.uuid4(), ipo_id=ipo.id)
            if ipo_data.details.company_overview is not None:
                ipo.details.company_overview = ipo_data.details.company_overview
            if ipo_data.details.business_model is not None:
                ipo.details.business_model = ipo_data.details.business_model
            if ipo_data.details.promoters is not None:
                ipo.details.promoters = ipo_data.details.promoters
            if ipo_data.details.objectives is not None:
                ipo.details.objectives = ipo_data.details.objectives
            if ipo_data.details.financial_summary is not None:
                ipo.details.financial_summary = ipo_data.details.financial_summary

        import datetime
        ipo.updated_at = datetime.datetime.now(datetime.timezone.utc)
        db.commit()
        db.refresh(ipo)
        return ipo

    def delete(self, db: Session, ipo: IPO) -> None:
        db.delete(ipo)
        db.commit()

ipo_repository = IPORepository()

