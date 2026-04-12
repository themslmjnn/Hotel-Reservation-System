from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.utils.model_constants import int_pk, str_20_uix_null_false, created_at, updated_at


class ServiceCategory(str, Enum):
    food = "food"
    beverage = "beverage"
    wellness = "wellness"
    entertainment = "entertainment"
    other = "other"

class Service(Base):
    __tablename__ = "services"

    id: Mapped[int_pk]

    name: Mapped[str_20_uix_null_false]
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    category: Mapped[ServiceCategory] = mapped_column(SQLEnum(ServiceCategory), nullable=False, default=ServiceCategory.other)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_available: Mapped[bool] = mapped_column(nullable=False, default=True)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    reservation_services: Mapped[list["ReservationService"]] = relationship(
        back_populates="service"
    )

class ReservationServiceStatus(str, Enum):
    active = "active"
    cancelled = "cancelled"
    delivered = "delivered"

class ReservationService(Base):
    __tablename__ = "reservation_services"

    id: Mapped[int_pk]

    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservations.id", ondelete="CASCADE"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"))

    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    cancellable_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    status: Mapped[ReservationServiceStatus] = mapped_column(SQLEnum(ReservationServiceStatus), nullable=False, default=ReservationServiceStatus.active)
    ordered_at: Mapped[created_at]

    reservation: Mapped["Reservation"] = relationship(
        back_populates="reservation_services"
    )

    service: Mapped["Service"] = relationship(
        back_populates="reservation_services"
    )