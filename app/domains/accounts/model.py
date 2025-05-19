from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from decimal import Decimal


@dataclass
class Account:
    id: UUID
    user_id: UUID
    currency: str
    balance: Decimal
    created_at: datetime
