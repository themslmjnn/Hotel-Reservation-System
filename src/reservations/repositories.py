from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from reservations.schemas import ReservationRoomCreate, ReservationSearch
from rooms.models import Room
from src.reservations.models import Reservation, ReservationRoom, ReservationStatus



class ReservationRepositoryAdmin:
    @staticmethod
    def add_reservation(db: AsyncSession, new_reservation: Reservation) -> None:
        db.add(new_reservation)

    @staticmethod
    async def get_conflicting_rooms(
        db: AsyncSession,
        room_ids: list[int],
        check_in_date: datetime,
        check_out_date: datetime,
    ) -> list[Room]:
        
        query = (select(Room)
            .join(ReservationRoom, ReservationRoom.room_id == Room.id)
            .join(Reservation, Reservation.id == ReservationRoom.reservation_id)
            .where(
                and_(
                    Room.id.in_(room_ids),
                    Reservation.check_out_date > check_in_date,
                    Reservation.check_in_date < check_out_date,
                    Reservation.status != ReservationStatus.cancelled,
                )
            )
        )
        result = await db.execute(query)

        return result.scalars().all()
    

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Reservation]:
        result = await db.execute(
            select(Reservation).options(selectinload(Reservation.rooms))
        )
        return result.scalars().all()


    @staticmethod
    async def get_by_id(db: AsyncSession, reservation_id: int) -> Reservation | None:
        result = await db.execute(
            select(Reservation)
            .options(selectinload(Reservation.rooms))
            .where(Reservation.id == reservation_id)
        )
        return result.scalar_one_or_none()


    @staticmethod
    async def get_by_owner(db: AsyncSession, owner_id: int) -> list[Reservation]:
        result = await db.execute(
            select(Reservation)
            .options(selectinload(Reservation.rooms))
            .where(Reservation.owner_id == owner_id)
        )
        return result.scalars().all()


    @staticmethod
    async def search(
        db: AsyncSession,
        search_request: ReservationSearch,
        owner_id: int | None = None,
    ) -> list[Reservation]:
        query = select(Reservation).options(selectinload(Reservation.rooms))

        if owner_id is not None:
            query = query.where(Reservation.owner_id == owner_id)

        if search_request.status:
            query = query.where(Reservation.status == search_request.status)

        if search_request.check_in_date:
            query = query.where(Reservation.check_in_date >= search_request.check_in_date)

        if search_request.check_out_date:
            query = query.where(Reservation.check_out_date <= search_request.check_out_date)

        if search_request.owner_id and owner_id is None:
            query = query.where(Reservation.owner_id == search_request.owner_id)

        result = await db.execute(query)
        return result.scalars().all()
    

class ReservationRoomRepository:
    @staticmethod
    def add_reservation_room(db: AsyncSession, new_reservation_room: ReservationRoomCreate) -> None:
        db.add(new_reservation_room)