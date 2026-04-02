from datetime import date, datetime
from enum import Enum

from sqlalchemy import DateTime, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.utils.model_constants import int_pk, str_30


class UserRole(str, Enum):
    admin = "admin"
    staff = "staff"
    guest = "guest"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]

    username: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    first_name: Mapped[str_30]
    last_name: Mapped[str_30]

    date_of_birth: Mapped[date] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=False)

    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    phone_number: Mapped[str_30]
    password_hash: Mapped[str] = mapped_column(nullable=False)

    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), index=True, nullable=False, default=UserRole.guest)

    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="owner") # type: ignore