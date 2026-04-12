from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.utils.model_constants import int_pk, created_at


class DeferredPaymentStatus(str, Enum):
    pending = "pending"
    settled = "settled"

class DeferredPayment(Base):
    __tablename__ = "deferred_payments"

    id: Mapped[int_pk]

    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservations.id", ondelete="CASCADE"))
    guest_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    amount_owed: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[DeferredPaymentStatus] = mapped_column(SQLEnum(DeferredPaymentStatus), nullable=False, default=DeferredPaymentStatus.pending)

    settled_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    settled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    notes: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[created_at]
    
    reservation: Mapped["Reservation"] = relationship(
        back_populates="deferred_payments"
    )
    
    guest: Mapped["User"] = relationship(
        back_populates="guest_deferred_payments",
        foreign_keys=[guest_id]
    )

    settler: Mapped["User | None"] = relationship(
        back_populates="settled_deferred_payments",
        foreign_keys=[settled_by]
    )