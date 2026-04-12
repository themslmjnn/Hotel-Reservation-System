from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.rooms.models import Room
from src.rooms.repository import (
    RoomRepositoryAdmin,
    RoomRepositoryPublic,
)
from src.rooms.schemas import (
    CreateRoomAdmin,
    SearchRoom,
    UpdateRoomRequest,
)
from src.utils.exception_constants import HTTP404
from src.utils.exceptions import check_uq_room_name
from src.utils.helpers import ensure_exists, update_object


class RoomServiceAdmin:
    @staticmethod
    async def create_room(db: AsyncSession, room_request: CreateRoomAdmin) -> Room:
        new_room = Room(
            name=room_request.name,
            type=room_request.type,
            price_per_night=room_request.price_per_night,
            status=room_request.status,
        )

        try:
            RoomRepositoryAdmin.add_room(db, new_room)

            await db.commit()
            await db.refresh(new_room)

            return new_room
        except IntegrityError as e:
            check_uq_room_name(e)
            raise

    @staticmethod
    async def update_room(db: AsyncSession, room_id: int, update_request: UpdateRoomRequest) -> Room:
        room = await RoomRepositoryPublic.get_room_by_id(db, room_id)
        ensure_exists(room, HTTP404.ROOM)

        try:
            update_object(room, update_request)

            await db.commit()
            await db.refresh(room)

            return room
        except IntegrityError as e:
            check_uq_room_name(e)
            raise

    @staticmethod
    async def delete_room(db: AsyncSession, room_id: int) -> None:
        room = await RoomRepositoryPublic.get_room_by_id(db, room_id)
        ensure_exists(room, HTTP404.ROOM)

        await RoomRepositoryAdmin.delete_room(room)
        await db.commit()


class RoomServicePublic:
    @staticmethod
    async def get_rooms(db: AsyncSession) -> list[Room]:
        return await RoomRepositoryPublic.get_rooms(db)

    @staticmethod
    async def search_rooms(db: AsyncSession, search_request: SearchRoom) -> list[Room]:
        return await RoomRepositoryPublic.search_rooms(db, search_request)

    @staticmethod
    async def get_room_by_id(db: AsyncSession, room_id: int) -> Room:
        room = await RoomRepositoryPublic.get_room_by_id(db, room_id)
        ensure_exists(room, HTTP404.ROOM)

        return room