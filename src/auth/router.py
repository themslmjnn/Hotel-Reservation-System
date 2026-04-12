from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.schemas import (
    AccountActivationRequest,
    LoginReponse,
    RefreshRequest,
    RefreshResponse,
)
from src.auth.service import AuthService
from src.core.depedencies import async_db_dependency, current_user_dependency


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login", response_model=LoginReponse, status_code=status.HTTP_200_OK)
async def login(
    db: async_db_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return await AuthService.login(db, form_data.username, form_data.password)


@router.post("/activate", status_code=status.HTTP_204_NO_CONTENT)
async def activate(
    db: async_db_dependency,
    acccount_activation_request: AccountActivationRequest,
):
    await AuthService.activate_account(db, acccount_activation_request)


@router.post("/refresh", response_model=RefreshResponse, status_code=status.HTTP_200_OK)
async def refresh(
    db: async_db_dependency,
    refresh_request: RefreshRequest,
):
    return await AuthService.refresh_token(db, refresh_request)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    db: async_db_dependency,
    current_user: current_user_dependency,
):
    await AuthService.logout(db, current_user)