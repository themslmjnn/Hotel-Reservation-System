from pydantic import BaseModel, Field
from datetime import datetime
from src.rooms.models import RoomType, RoomStatus
from src.utils.base_schema import BaseSchema


class RoomBase(BaseModel):
    name: str = Field(min_length=2, max_length=20)
    type: RoomType
    price: float = Field(gt=0)


class RoomCreate(RoomBase):
    status: RoomStatus = RoomStatus.available


class RoomResponse(RoomBase, BaseSchema):
    id: int
    status: RoomStatus
    created_at: datetime


class RoomUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=20)
    type: RoomType | None = None
    price: float | None = Field(default=None, gt=0)
    status: RoomStatus | None = None


class RoomUpdateResponse(RoomBase, BaseSchema):
    id: int
    status: RoomStatus
    updated_at: datetime


class RoomSearch(BaseModel):
    name: str | None = None
    type: RoomType | None = None
    status: RoomStatus | None = None
    min_price: float | None = Field(default=None, gt=0)
    max_price: float | None = Field(default=None, gt=0)