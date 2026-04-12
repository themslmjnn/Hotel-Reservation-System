from datetime import datetime

from pydantic import BaseModel, Field

from src.rooms.models import RoomStatus, RoomType
from src.utils.base_schema import BaseSchema


class RoomBase(BaseModel):
    name: str = Field(min_length=2, max_length=20)
    type: RoomType
    price_per_night: float = Field(gt=0)
    capacity: int | None = None

class CreateRoomAdmin(RoomBase):
    status: RoomStatus | None = RoomStatus.available

class RoomResponseBase(RoomBase, BaseSchema):
    id: int
    status: RoomStatus
    
class RoomResponseAdmin(RoomResponseBase):
    created_at: datetime
    update_at: datetime


class UpdateRoomRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=20)
    type: RoomType | None = None
    price_per_night: float | None = Field(default=None, gt=0)
    capacity: int | None = None
    status: RoomStatus | None = None


class SearchRoom(BaseModel):
    name: str | None = None
    type: RoomType | None = None
    status: RoomStatus | None = None
    min_price: float | None = Field(default=None, gt=0)
    max_price: float | None = Field(default=None, gt=0)