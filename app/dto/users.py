from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdateDTO(BaseModel):
    username: str


class UserReadDTO(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    role: str
    created_at: datetime
