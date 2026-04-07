from fastapi import APIRouter, status

from src.core.depedencies import async_db_dependency, current_user_dependency

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("", response_model=UserResponseAdmin, status_code=status.HTTP_201_CREATED) # type: ignore
def create_user(

):
    pass



# @router.get("", response_model=UserResponseAdmin, status_code=status.HTTP_200_OK) # type: ignore
