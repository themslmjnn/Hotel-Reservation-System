from fastapi import HTTPException, status
from src.utils.exception_constants import MESSAGE_403_FORBIDDEN

def ensure_exists(object, message) -> None:
    if object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
     

def update_object(instance, request) -> None:
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(instance, field, value)


def require_user(user, owner_id) -> None:
    if user["id"] != owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=MESSAGE_403_FORBIDDEN)