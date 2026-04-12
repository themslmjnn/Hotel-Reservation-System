from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.core.depedencies import async_db_dependency
from src.rooms.schemas import RoomResponseBase, SearchRoom
from src.rooms.service import RoomServicePublic

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms - Public"]
)

@router.get("", response_model=list[RoomResponseBase], status_code=status.HTTP_200_OK)
async def get_rooms(
    db: async_db_dependency,
):
    return await RoomServicePublic.get_rooms(db)


@router.get("/search", response_model=list[RoomResponseBase])
async def search_rooms(
    db: async_db_dependency,
    search_request: Annotated[SearchRoom, Depends()],
):
    return await RoomServicePublic.search_rooms(db, search_request)


@router.get("/{room_id}", response_model=RoomResponseBase)
async def get_room_by_id(
    db: async_db_dependency,
    room_id: int,
):
    return await RoomServicePublic.get_room_by_id(db, room_id)