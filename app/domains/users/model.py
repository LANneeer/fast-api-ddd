from uuid import UUID
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: UUID
    username: str
    email: str
    hashed_password: str
    role: str
    created_at: datetime
