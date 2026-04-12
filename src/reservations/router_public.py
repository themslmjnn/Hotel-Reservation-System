router = APIRouter(prefix="/reservations", tags=["Reservations - Public"])


@router.post("/me", response_model=ReservationResponsePublic, status_code=status.HTTP_201_CREATED)
async def create_my_reservation(
    db: async_db_dependency,
    reservation_request: ReservationCreatePublic,
    current_user: current_user_dependency,
):
    return await ReservationServicePublic.create_reservation(db, reservation_request, current_user)


@router.get("/me", response_model=list[ReservationResponsePublic])
async def get_my_reservations(
    db: async_db_dependency,
    current_user: current_user_dependency,
):
    return await ReservationServicePublic.get_my_reservations(db, current_user)


@router.get("/me/search", response_model=list[ReservationResponsePublic])
async def search_my_reservations(
    db: async_db_dependency,
    search_request: Annotated[ReservationSearch, Depends()],
    current_user: current_user_dependency,
):
    return await ReservationServicePublic.search_my_reservations(db, search_request, current_user)


@router.get("/me/{reservation_id}", response_model=ReservationResponsePublic)
async def get_my_reservation_by_id(
    db: async_db_dependency,
    reservation_id: int,
    current_user: current_user_dependency,
):
    return await ReservationServicePublic.get_my_reservation_by_id(db, reservation_id, current_user)