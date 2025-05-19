from app.domains.accounts.abstration import IAccountRepository
from app.infrastructure.accounts.orm import AccountsORM
from app.domains.accounts.model import Account
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID


class AccountRepository(IAccountRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    def _to_domain(self, row: AccountsORM) -> Account:
        return Account(
            id=row.id,
            user_id=row.user_id,
            currency=row.currency,
            balance=row.balance,
            created_at=row.created_at,
        )

    async def create(self, account: Account) -> Account:
        db_account = AccountsORM(**account.__dict__)
        self.db.add(db_account)
        await self.db.commit()
        await self.db.refresh(db_account)
        return self._to_domain(db_account)

    async def list_by_user(self, user_id: UUID):
        result = await self.db.execute(
            select(AccountsORM).where(AccountsORM.user_id == user_id)
        )
        return [self._to_domain(row) for row in result.scalars().all()]

    async def get_by_id(self, account_id: UUID) -> Account | None:
        result = await self.db.execute(
            select(AccountsORM).where(AccountsORM.id == account_id)
        )
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def delete(self, account_id: UUID) -> None:
        obj = await self.db.get(AccountsORM, account_id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()

    async def save(self, account: Account) -> Account:
        db_account = await self.db.get(AccountsORM, account.id)
        db_account.currency = account.currency
        await self.db.commit()
        await self.db.refresh(db_account)
        return self._to_domain(db_account)
