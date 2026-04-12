from fastapi import APIRouter, status

from src.core.depedencies import async_db_dependency, current_user_dependency
from src.users.schemas import (
    CreateUserGuest,
    UpdateUserAdmin,
    UpdateUserPasswordPublic,
    UserResponseBase,
)
from src.users.service import UserServiceGuest

router = APIRouter(
    prefix="/users",
    tags=["Users - Public"]
)

@router.post("", response_model=UserResponseBase, status_code=status.HTTP_201_CREATED)
async def create_account(
    db: async_db_dependency,
    user_request: CreateUserGuest,
):
    return await UserServiceGuest.create_account(db, user_request)


@router.get("/me", response_model=UserResponseBase, status_code=status.HTTP_200_OK)
async def get_me(
    current_user: current_user_dependency,
):
    return await current_user


@router.patch("/me", response_model=UserResponseBase, status_code=status.HTTP_200_OK)
async def update_me(
    db: async_db_dependency,
    update_request: UpdateUserAdmin,
    current_user: current_user_dependency,
):
    return await UserServiceGuest.update_me(db, update_request, current_user)


@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_my_password(
    db: async_db_dependency,
    password_request: UpdateUserPasswordPublic,
    current_user: current_user_dependency,
):
    await UserServiceGuest.update_my_password(db, password_request, current_user)