from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.reservations.repositories import ReservationRepositoryAdmin, ReservationRoomRepository
from src.reservations.schemas import ReservationCreateAdmin
from src.reservations.models import Reservation, ReservationRoom, ReservationStatus
from src.rooms.repository import RoomRepository
from src.utils.exception_constants import message_404_room
from src.utils.helpers import ensure_exists
from users.models import User


VALID_TRANSITIONS = {
    ReservationStatus.pending:     [ReservationStatus.confirmed, ReservationStatus.cancelled],
    ReservationStatus.confirmed:   [ReservationStatus.checked_in, ReservationStatus.cancelled],
    ReservationStatus.checked_in:  [ReservationStatus.checked_out],
    ReservationStatus.checked_out: [],
    ReservationStatus.cancelled:   [],
}

class ReservationServiceAdmin:
    @staticmethod
    async def create_reservation(db: AsyncSession, reservation_request: ReservationCreateAdmin) -> Reservation:
        for room_id in reservation_request.room_ids:
            room = await RoomRepository.get_room_by_id(db, room_id)

            ensure_exists(room, message_404_room(room_id))

        conflicting = await ReservationRepositoryAdmin.get_conflicting_rooms(
            db, reservation_request.room_ids, reservation_request.check_in_date, reservation_request.check_out_date
        )

        if conflicting:
            conflicting_names = [room.name for room in conflicting]
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Rooms already booked for this period: {', '.join(conflicting_names)}",
            )

        new_reservation = Reservation(
            owner_id=reservation_request.owner_id,
            check_in_date=reservation_request.check_in_date,
            check_out_date=reservation_request.check_out_date,
        )

        try:
            ReservationRepositoryAdmin.add_reservation(db, new_reservation)

            await db.flush()

            for room_id in reservation_request.room_ids:
                new_reservation_room = ReservationRoom(
                    reservation_id=new_reservation.id,
                    room_id=room_id
                )

                ReservationRoomRepository.add_reservation(db, new_reservation_room)

            await db.commit()
            result = await db.execute(
                select(Reservation)
                .options(selectinload(Reservation.rooms))
                .where(Reservation.id == new_reservation.id)
            )
            return result.scalar_one()
        except IntegrityError as e:
            print(e)
            raise

     @staticmethod
    async def get_all(db: AsyncSession) -> list[Reservation]:
        return await ReservationRepositoryAdmin.get_all(db)

    @staticmethod
    async def get_by_id(db: AsyncSession, reservation_id: int) -> Reservation:
        reservation = await ReservationRepositoryAdmin.get_by_id(db, reservation_id)
        ensure_exists(reservation, MESSAGE_404_RESERVATION)
        return reservation

    @staticmethod
    async def search(db: AsyncSession, search_request: ReservationSearch) -> list[Reservation]:
        return await ReservationRepositoryAdmin.search(db, search_request)

    @staticmethod
    async def update_status(
        db: AsyncSession,
        reservation_id: int,
        update_request: ReservationUpdateRequest,
    ) -> Reservation:
        reservation = await ReservationRepositoryAdmin.get_by_id(db, reservation_id)
        ensure_exists(reservation, MESSAGE_404_RESERVATION)

        allowed = VALID_TRANSITIONS[reservation.status]
        if update_request.status not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition from {reservation.status} to {update_request.status}",
            )

        reservation.status = update_request.status
        await db.commit()

        result = await db.execute(
            select(Reservation)
            .options(selectinload(Reservation.rooms))
            .where(Reservation.id == reservation.id)
        )
        return result.scalar_one()

    @staticmethod
    async def delete(db: AsyncSession, reservation_id: int) -> None:
        reservation = await ReservationRepositoryAdmin.get_by_id(db, reservation_id)
        ensure_exists(reservation, MESSAGE_404_RESERVATION)
        await db.delete(reservation)
        await db.commit()


class ReservationServicePublic:

    @staticmethod
    async def create_reservation(
        db: AsyncSession,
        reservation_request: ReservationCreatePublic,
        current_user: User,
    ) -> Reservation:
        for room_id in reservation_request.room_ids:
            room = await RoomRepository.get_room_by_id(db, room_id)
            ensure_exists(room, message_404_room(room_id))

        conflicting = await ReservationRepositoryAdmin.get_conflicting_rooms(
            db,
            reservation_request.room_ids,
            reservation_request.check_in_date,
            reservation_request.check_out_date,
        )

        if conflicting:
            conflicting_names = [room.name for room in conflicting]
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Rooms already booked for this period: {', '.join(conflicting_names)}",
            )

        new_reservation = Reservation(
            owner_id=current_user.id,
            check_in_date=reservation_request.check_in_date,
            check_out_date=reservation_request.check_out_date,
        )

        try:
            ReservationRepositoryAdmin.add_reservation(db, new_reservation)
            await db.flush()

            for room_id in reservation_request.room_ids:
                ReservationRoomRepository.add_reservation_room(
                    db,
                    ReservationRoom(
                        reservation_id=new_reservation.id,
                        room_id=room_id,
                    ),
                )

            await db.commit()
            result = await db.execute(
                select(Reservation)
                .options(selectinload(Reservation.rooms))
                .where(Reservation.id == new_reservation.id)
            )
            return result.scalar_one()

        except IntegrityError as e:
            print(e)
            raise

    @staticmethod
    async def get_my_reservations(db: AsyncSession, current_user: User) -> list[Reservation]:
        return await ReservationRepositoryAdmin.get_by_owner(db, current_user.id)

    @staticmethod
    async def get_my_reservation_by_id(
        db: AsyncSession,
        reservation_id: int,
        current_user: User,
    ) -> Reservation:
        reservation = await ReservationRepositoryAdmin.get_by_id(db, reservation_id)
        ensure_exists(reservation, MESSAGE_404_RESERVATION)

        if reservation.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this reservation",
            )
        return reservation

    @staticmethod
    async def search_my_reservations(
        db: AsyncSession,
        search_request: ReservationSearch,
        current_user: User,
    ) -> list[Reservation]:
        return await ReservationRepositoryAdmin.search(
            db, search_request, owner_id=current_user.id
        )