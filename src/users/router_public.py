from fastapi import APIRouter, status

from src.core.depedencies import async_db_dependency, current_user_dependency
from src.users.schemas import UserResponsePublic, UserUpdateAdmin, UserUpdatePasswordPublic, UserUpdateResponseAdmin
from src.users.service import UserServicePublic

router = APIRouter(
    prefix="/users",
    tags=["Users - Public"]
)


@router.get("/me", response_model=UserResponsePublic, status_code=status.HTTP_200_OK)
def get_me(current_user: current_user_dependency,):
    return current_user


@router.patch("/me", response_model=UserUpdateResponseAdmin, status_code=status.HTTP_200_OK)
async def update_me(
    db: async_db_dependency,
    update_request: UserUpdateAdmin,
    current_user: current_user_dependency,
):
    return await UserServicePublic.update_me(db, current_user, update_request)


@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_my_password(
    db: async_db_dependency,
    current_user: current_user_dependency,
    password_request: UserUpdatePasswordPublic,
):
    await UserServicePublic.update_my_password(db, current_user, password_request)