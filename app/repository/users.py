from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domains.users.abstraction import IUserRepository
from app.domains.users.model import User
from app.infrastructure.users.orm import Users as UsersORM


class UserRepository(IUserRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def _to_domain(self, db_user: UsersORM) -> User:
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            role=db_user.role,
            created_at=db_user.created_at,
        )

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.db.execute(select(UsersORM).where(UsersORM.id == user_id))
        db_user = result.scalars().one_or_none()
        return self._to_domain(db_user) if db_user else None

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(UsersORM).where(UsersORM.email == email))
        db_user = result.scalars().one_or_none()
        return self._to_domain(db_user) if db_user else None

    async def save(self, user: User) -> User:
        db_user = UsersORM(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            role=user.role,
            created_at=user.created_at,
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return self._to_domain(db_user)

    async def delete(self, user_id: UUID) -> None:
        obj = await self.db.get(UsersORM, user_id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()

    async def list_users(self, skip: int, limit: int) -> List[User]:
        result = await self.db.execute(select(UsersORM).offset(skip).limit(limit))
        return [self._to_domain(user) for user in result.scalars().all()]
