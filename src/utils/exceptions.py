from fastapi import HTTPException, status

from src.utils.exception_constants import MESSAGE_409_EMAIL, MESSAGE_409_USERNAME


def check_unique_username_error(e):
    if "ix_users_username" in str(e.orig):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=MESSAGE_409_USERNAME)


def check_unique_email_error(e):
    if "ix_users_email_address" in str(e.orig):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=MESSAGE_409_EMAIL)