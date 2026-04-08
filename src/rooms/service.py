from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.rooms.models import Room
from src.rooms.schemas import RoomCreate, RoomSearch, RoomUpdateRequest
from src.rooms.repository import RoomRepository
from src.utils.helpers import update_object, ensure_exists
from src.utils.exception_constants import MESSAGE_404_ROOM
from src.utils.exceptions import check_unique_name_error


class RoomService:
    @staticmethod
    async def add_room(db: AsyncSession, room_request: RoomCreate) -> Room:
        new_room = Room(
            name=room_request.name,
            type=room_request.type,
            price=room_request.price,
            status=room_request.status,
        )

        try:
            RoomRepository.add_room(db, new_room)

            await db.commit()
            await db.refresh(new_room)

            return new_room

        except IntegrityError as e:
            check_unique_name_error(e)

            raise

    @staticmethod
    async def get_all_rooms(db: AsyncSession) -> list[Room]:
        return await RoomRepository.get_all_rooms(db)

    @staticmethod
    async def get_room_by_id(db: AsyncSession, room_id: int) -> Room:
        room = await RoomRepository.get_room_by_id(db, room_id)
        ensure_exists(room, MESSAGE_404_ROOM)
        return room

    @staticmethod
    async def search_rooms(db: AsyncSession, search_request: RoomSearch) -> list[Room]:
        return await RoomRepository.search_rooms(db, search_request)

    @staticmethod
    async def update_room(db: AsyncSession, room_id: int, update_request: RoomUpdateRequest) -> Room:
        room = await RoomRepository.get_room_by_id(db, room_id)
        ensure_exists(room, MESSAGE_404_ROOM)

        try:
            update_object(room, update_request)

            await db.commit()
            await db.refresh(room)

            return room
        except IntegrityError as e:
            check_unique_name_error(e)

            raise

    @staticmethod
    async def delete_room(db: AsyncSession, room_id: int) -> None:
        room = await RoomRepository.get_room_by_id(db, room_id)

        ensure_exists(room, MESSAGE_404_ROOM)

        await RoomRepository.delete_room(room)
        await db.commit()