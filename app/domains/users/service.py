from datetime import datetime
from uuid import UUID, uuid4
from passlib.context import CryptContext

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .abstraction import IUserRepository, IUserService
from .model import User
from app.dto.users import UserCreateDTO, UserReadDTO


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(IUserService):
    def __init__(self, repo: IUserRepository) -> None:
        self._repo = repo

    async def register(self, data: UserCreateDTO) -> User:
        existing = await self._repo.get_by_email(data.email)
        if existing:
            raise ValueError("User already exists")
        user = User(
            id=uuid4(),
            username=data.username,
            email=data.email,
            hashed_password=pwd_context.hash(data.password),
            role="user",
            created_at=datetime.utcnow(),
        )
        return await self._repo.save(user=user)

    async def get_user_by_id(self, user_id: UUID) -> User:
        return await self._repo.get_by_id(user_id=user_id)

    async def get_by_email(self, email: str) -> User:
        return await self._repo.get_by_email(email)

    async def get_user_by_email(self, email: str) -> User:
        return await self._repo.get_by_email(email)

    async def get_all_users(self, skip: int = 0, limit: int = 10) -> list[User]:
        return await self._repo.list_users(skip, limit)

    async def authenticate(self, email: str, password: str) -> bool:
        user = await self._repo.get_by_email(email)
        if not user:
            return False
        return pwd_context.verify(password, user.hashed_password)

    async def update_username(self, user_id: UUID, new_username: str) -> User:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        user.username = new_username
        return await self._repo.save(user)

    async def delete_user(self, user_id: UUID):
        await self._repo.delete(user_id)

    async def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)
