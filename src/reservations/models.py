from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.utils.model_constants import int_pk


class ReservationStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    checked_in = "checked_in"
    checked_out = "checked_out"
    cancelled = "cancelled"

class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int_pk]

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    check_in_date: Mapped[datetime] = mapped_column(nullable=False)
    check_out_date: Mapped[datetime] = mapped_column(nullable=False)

    status: Mapped[ReservationStatus] = mapped_column(SQLEnum(ReservationStatus), nullable=False, default=ReservationStatus.pending)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    owner: Mapped["User"] = relationship(back_populates="reservations") # type: ignore
    reservation_rooms: Mapped[list["ReservationRoom"]] = relationship(back_populates="reservation", cascade="all, delete-orphan")
    rooms: Mapped[list["Room"]] = relationship(secondary="reservation_rooms",viewonly=True) # type: ignore

class ReservationRoom(Base):
    __tablename__ = "reservation_rooms"

    id: Mapped[int_pk]

    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservations.id", ondelete="CASCADE"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))

    reservation: Mapped["Reservation"] = relationship(back_populates="reservation_rooms")
    room: Mapped["Room"] = relationship(back_populates="reservation_rooms") # type: ignore