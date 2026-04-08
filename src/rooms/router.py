from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.rooms.schemas import RoomCreate, RoomResponse, RoomSearch, RoomUpdateRequest, RoomUpdateResponse
from src.rooms.service import RoomService
from src.users.models import User, UserRole
from src.core.depedencies import async_db_dependency, require_roles

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def add_room(
    db: async_db_dependency,
    room_request: RoomCreate,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    return await RoomService.add_room(db, room_request)


@router.get("", response_model=list[RoomResponse])
async def get_all_rooms(
    db: async_db_dependency,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    return await RoomService.get_all_rooms(db)

@router.get("/{room_id}", response_model=RoomResponse)
async def get_room_by_id(
    db: async_db_dependency,
    room_id: int,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    return await RoomService.get_room_by_id(db, room_id)


@router.get("/search", response_model=list[RoomResponse])
async def search_rooms(
    db: async_db_dependency,
    search_request: Annotated[RoomSearch, Depends()],
):
    return await RoomService.search_rooms(db, search_request)


@router.patch("/{room_id}", response_model=RoomUpdateResponse)
async def update_room(
    db: async_db_dependency,
    room_id: int,
    update_request: RoomUpdateRequest,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    return await RoomService.update_room(db, room_id, update_request)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    db: async_db_dependency,
    room_id: int,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    await RoomService.delete_room(db, room_id)