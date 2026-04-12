from pydantic import BaseModel, model_validator, Field, field_validator
from reservations.models import ReservationStatus
from src.utils.base_schema import BaseSchema
from datetime import datetime
from src.rooms.schemas import RoomResponse


class ReservationBase(BaseModel):
    check_in_date: datetime
    check_out_date: datetime
    room_ids: list[int] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_dates(self) -> "ReservationCreateAdmin":
        if self.check_in_date >= self.check_out_date:
            raise ValueError("check_in_date must be before check_out_date")
        return self
    
    @field_validator("room_ids")
    @classmethod
    def validate_room_ids(cls, value: list[int]) -> list[int]:
        if len(value) != len(set(value)):
            raise ValueError("room_ids must not contain duplicates")
        return value

class ReservationCreateAdmin(ReservationBase):
    owner_id: int

class ReservationResponseAdmin(BaseSchema):
    id: int
    owner_id: int
    check_in_date: datetime
    check_out_date: datetime
    status: ReservationStatus
    rooms: list[RoomResponse]
    created_at: datetime


class ReservationCreatePublic(ReservationBase):
    pass

class ReservationResponsePublic(BaseSchema):
    id: int
    check_in_date: datetime
    check_out_date: datetime
    status: ReservationStatus
    rooms: list[RoomResponse]
    created_at: datetime


class ReservationRoomBase(BaseModel):
    reservation_id: int
    room_id: int

class ReservationRoomCreate(ReservationRoomBase):
    pass

class ReservationRoomResponse(ReservationBase, BaseSchema):
    id: int