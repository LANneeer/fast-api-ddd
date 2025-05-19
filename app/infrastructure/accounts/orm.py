from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime
from app.config import Base


class AccountsORM(Base):
    __tablename__ = "accounts"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    currency = Column(String(3), nullable=False)
    balance = Column(Numeric(18, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
