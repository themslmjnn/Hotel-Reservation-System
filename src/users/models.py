from datetime import date, datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.utils.model_constants import int_pk, str_20_uix_null_false, str_30_null_false


class UserRole(str, Enum):
    system_admin = "system_admin"
    administrator = "administrator"
    receptionist = "receptionist"
    guest = "guest"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]

    username: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=True)
    first_name: Mapped[str_30_null_false]
    last_name: Mapped[str_30_null_false]

    date_of_birth: Mapped[date] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    phone_number: Mapped[str_20_uix_null_false]
    password_hash: Mapped[str] = mapped_column(nullable=True)

    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), index=True, nullable=False, default=UserRole.guest)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    invite_token_hash: Mapped[str | None] = mapped_column(nullable=True)
    invite_token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    refresh_token_hash: Mapped[str | None] = mapped_column(nullable=True)
    refresh_token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    creator: Mapped["User | None"] = relationship(
        "User",
        remote_side="User.id",
        foreign_keys="[User.created_by]",
        back_populates="created_users"
    )

    created_users: Mapped[list["User"]] = relationship(
        "User",
        foreign_keys="[User.created_by]",
        back_populates="creator"
    )

    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="owner"
    )

    guest_deferred_payments: Mapped[list["DeferredPayment"]] = relationship(
        back_populates="guest",
        foreign_keys="[DeferredPayment.guest_id]"
    )

    settled_deferred_payments: Mapped[list["DeferredPayment"]] = relationship(
        back_populates="settler",
        foreign_keys="[DeferredPayment.settled_by]"
    )