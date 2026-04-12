from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.core.depedencies import async_db_dependency, require_roles
from src.users.models import User, UserRole
from src.users.schemas import (
    CreateUserStaff,
    SearchUserStaff,
    UserResponseBase,
    UserResponseStaff,
)
from src.users.service import UserServiceStaff

router = APIRouter(
    prefix="/users",
    tags=["Users - Staffs"]
)

@router.post("/guests", response_model=UserResponseBase, status_code=status.HTTP_201_CREATED)
async def create_guest(
    db: async_db_dependency,
    guest_request: CreateUserStaff,
    current_user: Annotated[User, Depends(require_roles(UserRole.receptionist))],
):
    return await UserServiceStaff.create_guest(db, guest_request, current_user)


@router.get("", response_model=list[UserResponseStaff], status_code=status.HTTP_200_OK)
async def get_guests(
    db: async_db_dependency,
    _: Annotated[User, Depends(require_roles(UserRole.receptionist))],
):
    return await UserServiceStaff.get_guests(db)


@router.get("/search", response_model=list[UserResponseStaff], status_code=status.HTTP_200_OK)
async def search_guests(
    db: async_db_dependency,
    search_request: Annotated[SearchUserStaff, Depends()],
    _: Annotated[User, Depends(require_roles(UserRole.receptionist))],
):
    return await UserServiceStaff.search_guests(db, search_request)