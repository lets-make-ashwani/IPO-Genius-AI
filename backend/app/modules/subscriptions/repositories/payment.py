from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
import uuid
from app.modules.subscriptions.models.payment import PaymentTransaction, PaymentStatus

class PaymentTransactionRepository:
    def get_by_id(self, db: Session, payment_id: uuid.UUID) -> Optional[PaymentTransaction]:
        return db.query(PaymentTransaction).filter(PaymentTransaction.id == payment_id).first()

    def get_by_provider_order_id(self, db: Session, order_id: str, lock: bool = False) -> Optional[PaymentTransaction]:
        query = db.query(PaymentTransaction).filter(PaymentTransaction.provider_order_id == order_id)
        if lock:
            query = query.with_for_update()
        return query.first()

    def get_by_provider_payment_id(self, db: Session, payment_id: str) -> Optional[PaymentTransaction]:
        return db.query(PaymentTransaction).filter(PaymentTransaction.provider_payment_id == payment_id).first()

    def list_by_user(
        self, db: Session, user_id: uuid.UUID, limit: int = 20, offset: int = 0
    ) -> Tuple[List[PaymentTransaction], int]:
        query = db.query(PaymentTransaction).filter(PaymentTransaction.user_id == user_id)
        total = query.count()
        results = query.order_by(PaymentTransaction.created_at.desc()).offset(offset).limit(limit).all()
        return results, total

    def create(self, db: Session, payment: PaymentTransaction) -> PaymentTransaction:
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    def update(self, db: Session, payment: PaymentTransaction) -> PaymentTransaction:
        db.commit()
        db.refresh(payment)
        return payment

    def list_all_paginated(
        self, db: Session, limit: int = 20, offset: int = 0
    ) -> Tuple[List[PaymentTransaction], int]:
        query = db.query(PaymentTransaction)
        total = query.count()
        results = query.order_by(PaymentTransaction.created_at.desc()).offset(offset).limit(limit).all()
        return results, total

payment_transaction_repository = PaymentTransactionRepository()
