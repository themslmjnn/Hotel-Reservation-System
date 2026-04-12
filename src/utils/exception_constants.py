from typing import Annotated

from fastapi import Path

MESSAGE_400_PASSWORD = "Incorrect old password"
MESSAGE_400_INVITE_TOKEN = "Account already activated or never invited"
MESSAGE_400_INVITE_TOKEN_EXPIRED = "Invite token expired"
MESSAGE_400_INVITE_TOKEN = "Invalid invite token"
MESSAGE_401_REFRESH_TOKEN = "Invalid refresh token"
MESSAGE_401_REFRESH_TOKEN_EXPIRED = "Invite token expired"
MESSAGE_401_UNAUTHORIZED = "Invalid credentials"
MESSAGE_401_INACTIVE = "Account not activated yet"
MESSAGE_403_FORBIDDEN = "Accessing denied"
MESSAGE_403_INACTIVE = "Deactivated account"
MESSAGE_404_USER = "User(s) not found"
MESSAGE_404_ROOM = "Room(s) not found"
MESSAGE_409_USERNAME = "Username already exists"
MESSAGE_409_EMAIL = "Email already exists"
MESSAGE_409_PHONE_NUMBER = "Phone number already exists"
MESSAGE_409_ROOM_NAME = "Room name already exists"
MESSAGE_TOKEN_ERR = "Invalid or expired token"


from typing import Annotated

from fastapi import Path


# --- Path Parameters ---
path_param_int_ge1 = Annotated[int, Path(ge=1)]

# --- HTTP 400 Bad Request ---
class HTTP400:
    INCORRECT_PASSWORD = "Incorrect old password."
    INVITE_TOKEN_USED = "Account already activated or was never invited."
    INVITE_TOKEN_EXPIRED = "Invite token has expired."
    INVITE_TOKEN_INVALID = "Invalid invite token."
    CANNOT_DELETE_ACTIVE_USER = "Cannot delete an active account. Deactivate first."
    CANNOT_DELETE_ROOM = "Cannot delete a room with active reservations."
    INVALID_STATUS_TRANSITION = "Invalid status transition."


# --- HTTP 401 Unauthorized ---
class HTTP401:
    INVALID_CREDENTIALS = "Invalid credentials."
    ACCOUNT_NOT_ACTIVATED = "Account has not been activated yet."
    REFRESH_TOKEN_INVALID = "Invalid refresh token."
    REFRESH_TOKEN_EXPIRED = "Refresh token has expired."
    TOKEN_INVALID = "Invalid or expired token."


# --- HTTP 403 Forbidden ---
class HTTP403:
    ACCESS_DENIED = "Access denied."
    ACCOUNT_DEACTIVATED = "Your account has been deactivated."
    CANNOT_MODIFY_AFTER_PAYMENT = "Reservation cannot be modified after payment."


# --- HTTP 404 Not Found ---
class HTTP404:
    USER = "User not found."
    ROOM = "Room not found."
    RESERVATION = "Reservation not found."
    SERVICE = "Service not found."
    DEFERRED_PAYMENT = "Deferred payment not found."


# --- HTTP 409 Conflict ---
class HTTP409:
    USERNAME = "Username already taken."
    EMAIL = "Email already taken."
    PHONE_NUMBER = "Phone number already taken."
    ROOM_NAME = "Room name already taken."
    ROOM_UNAVAILABLE = "One or more rooms are unavailable for the selected dates."