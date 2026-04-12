from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Numeric, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.utils.model_constants import int_pk, created_at, updated_at


class ReservationStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    checked_in = "checked_in"
    checked_out = "checked_out"
    cancelled = "cancelled"
    deferred = "deferred"

class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int_pk]

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    check_in_date: Mapped[datetime] = mapped_column(nullable=False)
    check_out_date: Mapped[datetime] = mapped_column(nullable=False)

    status: Mapped[ReservationStatus] = mapped_column(SQLEnum(ReservationStatus), nullable=False, default=ReservationStatus.pending)

    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    owner: Mapped["User"] = relationship(
        back_populates="reservations"
    )

    reservation_rooms: Mapped[list["ReservationRoom"]] = relationship(
        back_populates="reservation", 
        cascade="all, delete-orphan"
    )

    rooms: Mapped[list["Room"]] = relationship(
        secondary="reservation_rooms",
        viewonly=True
    )

    reservation_services: Mapped[list["ReservationService"]] = relationship(
        back_populates="reservation", 
        cascade="all, delete-orphan"
    ) 

    deferred_payment: Mapped["DeferredPayment | None"] = relationship(
        back_populates="reservation"
    )

class ReservationRoom(Base):
    __tablename__ = "reservation_rooms"

    id: Mapped[int_pk]

    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservations.id", ondelete="CASCADE"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))

    reservation: Mapped["Reservation"] = relationship(
        back_populates="reservation_rooms"
    )

    room: Mapped["Room"] = relationship(
        back_populates="reservation_rooms"
    ) 