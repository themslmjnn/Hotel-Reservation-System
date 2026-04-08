from fastapi import APIRouter, status, Depends
from typing import Annotated

from src.core.depedencies import async_db_dependency
from src.users.models import User, UserRole
from src.core.depedencies import require_roles
from src.users.schemas import UserCreateAdmin, UserResponseAdmin, UserSearch, UserUpdateAdmin, UserUpdatePasswordAdmin, UserUpdateResponseAdmin
from src.users.service import UserServiceAdmin
from src.utils.exception_constants import path_param_int_ge1

router = APIRouter(
    prefix="/users",
    tags=["Users - Admin"]
)


@router.post("", response_model=UserResponseAdmin, status_code=status.HTTP_201_CREATED)
async def create_user(
    db: async_db_dependency,
    user_request: UserCreateAdmin,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    return await UserServiceAdmin.create_user(db, user_request)


@router.get("", response_model=list[UserResponseAdmin], status_code=status.HTTP_200_OK)
async def get_all_users(
    db: async_db_dependency,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    return await UserServiceAdmin.get_all_users(db)


@router.get("/{user_id}", response_model=UserResponseAdmin, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    db: async_db_dependency,
    user_id: path_param_int_ge1,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    return await UserServiceAdmin.get_user_by_id(db, user_id)


@router.get("/search", response_model=list[UserResponseAdmin], status_code=status.HTTP_200_OK)
async def search_users(
    db: async_db_dependency,
    search_request: Annotated[UserSearch, Depends()],
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    return await UserServiceAdmin.search_users(db, search_request)


@router.delete("/{user_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user_by_id(
    db: async_db_dependency, 
    user_id: path_param_int_ge1,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    await UserServiceAdmin.deactivate_user_by_id(db, user_id)


@router.patch("/{user_id}/activate", status_code=status.HTTP_204_NO_CONTENT)
async def activate_account(
    db: async_db_dependency, 
    user_id: path_param_int_ge1,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    await UserServiceAdmin.activate_account(db, user_id)


@router.patch("/{user_id}", response_model=UserUpdateResponseAdmin, status_code=status.HTTP_200_OK)
async def update_user(
    db: async_db_dependency,
    user_id: int,
    update_request: UserUpdateAdmin,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    return await UserServiceAdmin.update_user(db, user_id, update_request)


@router.put("/{user_id}/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(
    db: async_db_dependency,
    user_id: int,
    password_request: UserUpdatePasswordAdmin,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    await UserServiceAdmin.update_password(db, user_id, password_request)