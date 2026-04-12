from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import decode_access_token
from src.database import AsyncSessionLocal
from src.users.models import User, UserRole
from src.users.repository import UserRepositoryBase
from src.utils.exception_constants import (
    MESSAGE_401_UNAUTHORIZED,
    MESSAGE_403_FORBIDDEN,
    MESSAGE_403_INACTIVE,
    MESSAGE_404_USER,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async_db_dependency = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    db: async_db_dependency,
    token: str = Depends(oauth2_scheme)
) -> User:

    try:
        payload = decode_access_token(token)

        user_id: int = int(payload.get("sub"))
        
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=MESSAGE_401_UNAUTHORIZED)

    user = await UserRepositoryBase.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404_USER)
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=MESSAGE_403_INACTIVE)
    
    return user

current_user_dependency = Annotated[User, Depends(get_current_user)]


def require_roles(*roles: UserRole):
    def guard(current_user: current_user_dependency) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=MESSAGE_403_FORBIDDEN,
            )
        
        return current_user
    return guard