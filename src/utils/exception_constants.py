from fastapi import Path

from typing import Annotated


MESSAGE_400_PASSWORD = "Incorrect old password"

MESSAGE_403_FORBIDDEN = "Accessing denied"

MESSAGE_404_USER = "User(s) not found"

def message_404_room(room_id: int) -> str: 
    return f"Room with {room_id=} not found"

MESSAGE_409_DUPLICATE = "Duplicate values are not accepted"
MESSAGE_409_USERNAME = "Username already taken"
MESSAGE_409_EMAIL = "Email already registered"

MESSAGE_403_INACTIVE = "Inactive user" 
MESSAGE_401_UNAUTHORIZED = "Could not validate credentials"
MESSAGE_TOKEN_ERR = "Invalid or expired token"

path_param_int_ge1 = Annotated[int, Path(ge=1)]