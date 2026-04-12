from decimal import Decimal
from enum import Enum

from sqlalchemy import Numeric, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.utils.model_constants import int_pk, str_20_uix_null_false, created_at, updated_at


class RoomType(str, Enum):
    single = "single"
    double = "double"
    suite = "suite"
    deluxe = "deluxe"
    other = "other"

class RoomStatus(str, Enum):
    available = "available"
    maintenance = "maintenance"

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int_pk]

    name: Mapped[str_20_uix_null_false]

    type: Mapped[RoomType] = mapped_column(SQLEnum(RoomType), nullable=False, default=RoomType.other)
    price_per_night: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    capacity: Mapped[int | None] = mapped_column(nullable=True)

    status: Mapped[RoomStatus] = mapped_column(SQLEnum(RoomStatus), nullable=False, default=RoomStatus.available)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    reservation_rooms: Mapped[list["ReservationRoom"]] = relationship(
        back_populates="room"
    )