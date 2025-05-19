from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.auth import LoginDTO, TokenDTO
from app.infrastructure.users.auth import create_access_token
from app.domains.users.service import UserService
from app.repository.users import UserRepository
from app.config import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenDTO)
async def login(data: LoginDTO, db: AsyncSession = Depends(get_db)):
    service = UserService(UserRepository(db))
    user = await service.get_by_email(data.email)
    if not user or not await service.verify_password(
        data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return TokenDTO(access_token=token)
