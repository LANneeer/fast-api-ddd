from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.infrastructure.users.dependencies import get_current_user
from app.dto.accounts import AccountCreateDTO, AccountReadDTO
from app.domains.accounts.service import AccountService
from app.repository.accounts import AccountRepository
from app.config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.users.model import User

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/", response_model=AccountReadDTO)
async def create_account(
    data: AccountCreateDTO,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AccountService(AccountRepository(db))
    account = await service.create_account(current_user.id, data)
    return AccountReadDTO(**account.__dict__)


@router.get("/", response_model=list[AccountReadDTO])
async def list_user_accounts(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    service = AccountService(AccountRepository(db))
    accounts = await service.list_by_user(current_user.id)
    return [AccountReadDTO(**a.__dict__) for a in accounts]


@router.get("/{account_id}", response_model=AccountReadDTO)
async def get_account(
    account_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AccountService(AccountRepository(db))
    account = await service.get_by_id(account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountReadDTO(**account.__dict__)


@router.put("/{account_id}", response_model=AccountReadDTO)
async def update_account(
    account_id: UUID,
    data: AccountCreateDTO,  # для примера: обновим валюту
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AccountService(AccountRepository(db))
    account = await service.get_by_id(account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Account not found")

    updated = await service.update_currency(account_id, data.currency)
    return AccountReadDTO(**updated.__dict__)


@router.delete("/{account_id}", status_code=204)
async def delete_account(
    account_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AccountService(AccountRepository(db))
    account = await service.get_by_id(account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Account not found")

    await service.delete(account_id)
