from pydantic import BaseModel, constr
from uuid import UUID
from decimal import Decimal
from datetime import datetime


class AccountCreateDTO(BaseModel):
    currency: constr(to_upper=True, min_length=3, max_length=3)


class AccountReadDTO(BaseModel):
    id: UUID
    user_id: UUID
    currency: str
    balance: Decimal
    created_at: datetime
