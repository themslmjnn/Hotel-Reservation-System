from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.repository import AuthRepository
from src.auth.schemas import (
    AccountActivationRequest,
    LoginReponse,
    RefreshRequest,
    RefreshResponse,
)
from src.core.depedencies import current_user_dependency
from src.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_password,
    verify_invite_token,
    verify_password,
    verify_refresh_token,
)
from src.utils.helpers import ensure_exists


REFRESH_TOKEN_EXPIRE_DAYS = 7

class AuthService:
    @staticmethod
    async def login(db: AsyncSession, identifier: str, password: str) -> LoginReponse:
        user = await AuthRepository.get_by_login_identifier(db, identifier)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if user.password_hash is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Account not activated yet",
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Deactivated account",
            )
        
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid Credentials",
            )
        
        access_token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role,
            }
        )

        raw_refresh_token, refresh_token_hash = generate_refresh_token()

        user.refresh_token_hash = refresh_token_hash
        user.refresh_token_expires_at = (
            datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

        await db.commit()

        return {
            "access_token": access_token, 
            "refresh_token": raw_refresh_token,
            "token_type": "bearer",
        }
    
    
    @staticmethod
    async def activate_account(db: AsyncSession, activation_request: AccountActivationRequest) -> None:
        user = await AuthRepository.get_by_login_identifier(db, activation_request.email)

        ensure_exists(user, "User not found")

        if user.invite_token_hash is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Account already activated or never invited",
            )
        
        if datetime.now(timezone.utc) > user.invite_token_expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Token expired",
            )
        
        if not verify_invite_token(activation_request.invite_token, user.invite_token_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Invalid token",
            )
        
        user.password_hash = hash_password(activation_request.password)
        user.is_active = True
        user.invite_token_hash = None
        user.invite_token_expires_at = None

        await db.commit()


    @staticmethod
    async def refresh_token(db: AsyncSession, refresh_request: RefreshRequest) -> RefreshResponse:
        user = await AuthRepository.get_by_id(db, refresh_request.user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid refresh token",
            )
        
        if user.refresh_token_hash is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid refresh token"
            )
        
        if datetime.now(timezone.utc) > user.refresh_token_expires_at:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Refresh token expired",
            )

        if not verify_refresh_token(refresh_request.refresh_token, user.refresh_token_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid refresh token",
            )
        
        access_token = create_access_token(
            {
                "sub": str(user.id), 
                "role": user.role,
            }
        )

        raw_refresh_token, refresh_token_hash = generate_refresh_token()

        user.refresh_token_hash = refresh_token_hash
        user.refresh_token_expires_at = (
            datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

        await db.commit()

        return {
            "access_token": access_token, 
            "refresh_token": raw_refresh_token,
            "token_type": "bearer",
        }
    

    @staticmethod
    async def logout(db: AsyncSession, current_user: current_user_dependency) -> None:
        current_user.refresh_token_hash = None
        current_user.refresh_token_expires_at = None

        await db.commit()