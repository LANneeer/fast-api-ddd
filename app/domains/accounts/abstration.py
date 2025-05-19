from abc import ABC, abstractmethod
from uuid import UUID
from app.domains.accounts.model import Account
from typing import List


class IAccountRepository(ABC):
    @abstractmethod
    async def create(self, account: Account) -> Account:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> List[Account]:
        raise NotImplementedError

    async def get_by_id(self, account_id: UUID) -> Account | None:
        raise NotImplementedError

    async def delete(self, account_id: UUID):
        raise NotImplementedError

    async def save(self, account: Account) -> Account:
        raise NotImplementedError
