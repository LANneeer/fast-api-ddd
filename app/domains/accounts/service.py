from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal
from app.domains.accounts.abstration import IAccountRepository
from app.dto.accounts import AccountCreateDTO
from app.domains.accounts.model import Account


class AccountService:
    def __init__(self, repo: IAccountRepository):
        self.repo = repo

    async def create_account(self, user_id: UUID, dto: AccountCreateDTO) -> Account:
        acc = Account(
            id=uuid4(),
            user_id=user_id,
            currency=dto.currency,
            balance=Decimal("0"),
            created_at=datetime.utcnow(),
        )
        return await self.repo.create(acc)

    async def list_by_user(self, user_id: UUID) -> list[Account]:
        return await self.repo.list_by_user(user_id)

    async def get_by_id(self, account_id: UUID) -> Account | None:
        return await self.repo.get_by_id(account_id)

    async def update_currency(self, account_id: UUID, new_currency: str) -> Account:
        account = await self.repo.get_by_id(account_id)
        account.currency = new_currency
        return await self.repo.save(account)

    async def delete(self, account_id: UUID):
        await self.repo.delete(account_id)
