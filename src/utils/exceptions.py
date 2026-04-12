from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.utils.exception_constants import MESSAGE_409_EMAIL, MESSAGE_409_USERNAME


def check_unique_username_error(e):
    if "ix_users_username" in str(e.orig):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=MESSAGE_409_USERNAME)


def check_unique_email_error(e):
    if "ix_users_email_address" in str(e.orig):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=MESSAGE_409_EMAIL)
    
def handle_user_integrity_error(e: IntegrityError) -> None:
    error_str = str(e.orig).lower()

    if "username" in error_str:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    if "email" in error_str:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )
    if "phone_number" in error_str:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number already exists",
        )