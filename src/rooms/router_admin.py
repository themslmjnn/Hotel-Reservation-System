from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.core.depedencies import async_db_dependency, require_roles
from src.rooms.schemas import (
    CreateRoomAdmin,
    RoomResponseAdmin,
    UpdateRoomRequest,
)
from src.rooms.service import RoomServiceAdmin
from src.users.models import User, UserRole

router = APIRouter(
    prefix="/rooms", 
    tags=["Rooms - Admin"])

@router.post("", response_model=RoomResponseAdmin, status_code=status.HTTP_201_CREATED)
async def create_room(
    db: async_db_dependency,
    room_request: CreateRoomAdmin,
    _: Annotated[User, Depends(require_roles((UserRole.system_admin, UserRole.administrator)))],
):
    return await RoomServiceAdmin.create_room(db, room_request)


@router.patch("/{room_id}", response_model=RoomResponseAdmin, status_code=status.HTTP_200_OK)
async def update_room(
    db: async_db_dependency,
    room_id: int,
    update_request: UpdateRoomRequest,
    _: Annotated[User, Depends(require_roles((UserRole.system_admin, UserRole.administrator)))],
):
    return await RoomServiceAdmin.update_room(db, room_id, update_request)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    db: async_db_dependency,
    room_id: int,
    _: Annotated[User, Depends(require_roles((UserRole.system_admin, UserRole.administrator)))],
):
    await RoomServiceAdmin.delete_room(db, room_id)