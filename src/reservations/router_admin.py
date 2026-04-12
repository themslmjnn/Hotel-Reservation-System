from typing import Annotated

from fastapi import APIRouter, Depends, status
from reservations.services import ReservationServiceAdmin
from src.core.depedencies import async_db_dependency, require_roles
from users.models import User, UserRole
from src.reservations.schemas import ReservationCreateAdmin, ReservationResponseAdmin

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations - Admin"]
)

router = APIRouter(prefix="/admin/reservations", tags=["Reservations - Admin"])


@router.post("", response_model=ReservationResponseAdmin, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    db: async_db_dependency,
    reservation_request: ReservationCreateAdmin,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.staff))],
):
    return await ReservationServiceAdmin.create_reservation(db, reservation_request)


@router.get("", response_model=list[ReservationResponseAdmin])
async def get_all_reservations(
    db: async_db_dependency,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.staff))],
):
    return await ReservationServiceAdmin.get_all(db)


@router.get("/search", response_model=list[ReservationResponseAdmin])
async def search_reservations(
    db: async_db_dependency,
    search_request: Annotated[ReservationSearch, Depends()],
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.staff))],
):
    return await ReservationServiceAdmin.search(db, search_request)


@router.get("/{reservation_id}", response_model=ReservationResponseAdmin)
async def get_reservation_by_id(
    db: async_db_dependency,
    reservation_id: int,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.staff))],
):
    return await ReservationServiceAdmin.get_by_id(db, reservation_id)


@router.patch("/{reservation_id}/status", response_model=ReservationResponseAdmin)
async def update_reservation_status(
    db: async_db_dependency,
    reservation_id: int,
    update_request: ReservationUpdateRequest,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    return await ReservationServiceAdmin.update_status(db, reservation_id, update_request)


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    db: async_db_dependency,
    reservation_id: int,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
):
    await ReservationServiceAdmin.delete(db, reservation_id)