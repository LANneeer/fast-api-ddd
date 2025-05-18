from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.dto.users import UserCreateDTO

from .model import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def save(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_users(self, skip: int, limit: int) -> List[User]:
        raise NotImplementedError


class IUserService(ABC):
    @abstractmethod
    async def register(self, data: UserCreateDTO) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def authenticate(self, email: str, password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update_username(self, user_id: UUID, new_username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, user_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def get_all_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        raise NotImplementedError
