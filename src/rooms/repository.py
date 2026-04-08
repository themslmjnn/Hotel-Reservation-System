from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.rooms.models import Room
from src.rooms.schemas import RoomSearch


class RoomRepository:
    @staticmethod
    def add_room(db: AsyncSession, room: Room) -> None:
        db.add(room)

    @staticmethod
    def delete_room(db: AsyncSession, room: Room) -> None:
        db.delete(room)


    @staticmethod
    async def get_all_rooms(db: AsyncSession) -> list[Room]:
        query = select(Room)

        result = await db.execute(query)

        return result.scalars().all()

    @staticmethod
    async def get_room_by_id(db: AsyncSession, room_id: int) -> Room | None:
        query = (
            select(Room)
            .where(Room.id == room_id)
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()

    @staticmethod
    async def search_rooms(db: AsyncSession, search_request: RoomSearch) -> list[Room]:
        query = select(Room)

        if search_request.name:
            query = query.filter(Room.name.ilike(f"%{search_request.name}%"))

        if search_request.type:
            query = query.filter(Room.type == search_request.type)

        if search_request.status:
            query = query.filter(Room.status == search_request.status)

        if search_request.min_price:
            query = query.filter(Room.price >= search_request.min_price)

        if search_request.max_price:
            query = query.filter(Room.price <= search_request.max_price)

        result = await db.execute(query)

        return result.scalars().all()