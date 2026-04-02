from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.utils.model_constants import int_pk


class RoomType(str, Enum):
    single = "single"
    double = "double"
    suite = "suite"
    deluxe = "deluxe"

class RoomStatus(str, Enum):
    available = "available"
    maintenance = "maintenance"

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int_pk]

    name: Mapped[str] = mapped_column(String(20), index=True, unique=True, nullable=False)

    type: Mapped[RoomType] = mapped_column(SQLEnum(RoomType), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2))

    status: Mapped[RoomStatus] = mapped_column(SQLEnum(RoomStatus), nullable=False, default=RoomStatus.available)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    reservation_rooms: Mapped[list["ReservationRoom"]] = relationship(back_populates="room") # type: ignore