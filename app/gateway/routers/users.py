from typing import List
from uuid import UUID
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.users.model import User
from app.domains.users.service import UserService
from app.dto.users import UserCreateDTO, UserReadDTO, UserUpdateDTO
from app.infrastructure.users.dependencies import get_current_user
from app.repository.users import UserRepository
from app.config import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserReadDTO)
async def register_user(data: UserCreateDTO, db: AsyncSession = Depends(get_db)):
    service = UserService(UserRepository(db))
    user = await service.register(data=data)
    return UserReadDTO(**user.__dict__)


@router.get("/me", response_model=UserReadDTO)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return UserReadDTO(**current_user.__dict__)


@router.get("/{user_id}", response_model=UserReadDTO)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    service = UserService(UserRepository(db))
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserReadDTO(**user.__dict__)


@router.get("/", response_model=List[UserReadDTO])
async def list_users(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    service = UserService(UserRepository(db))
    users = await service.get_all_users(skip, limit)
    return [UserReadDTO(**u.__dict__) for u in users]


@router.put("/{user_id}", response_model=UserReadDTO)
async def update_user(
    user_id: UUID, data: UserUpdateDTO, db: AsyncSession = Depends(get_db)
):
    service = UserService(UserRepository(db))
    try:
        user = await service.update_username(user_id, data.username)
        return UserReadDTO(**user.__dict__)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    service = UserService(UserRepository(db))
    await service.delete_user(user_id)
