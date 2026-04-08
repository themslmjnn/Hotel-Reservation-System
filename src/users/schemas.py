from pydantic import BaseModel, Field, EmailStr, field_validator

from typing import Optional
from datetime import date, datetime
from src.utils.schema_field_validator import validate_date_of_birth, validate_email, validate_password
from src.users.models import UserRole
from src.utils.base_schema import BaseSchema


class UserBase(BaseModel):
    username: str = Field(min_length=6, max_length=20)
    first_name: str = Field(min_length=2, max_length=20)
    last_name: str = Field(min_length=2, max_length=20)
    date_of_birth: date
    address: str | None = Field(max_length=100, default=None)
    email: EmailStr

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, field: date) -> date:
        return validate_date_of_birth(field)
    
    @field_validator("email")
    @classmethod
    def valdiate_email(cls, field: str) -> str:
        return validate_email(field)


class UserCreateAdmin(UserBase):
    password: str = Field(min_length=8)
    role: UserRole

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, field: str) -> str:
        return validate_password(field)


class UserResponseAdmin(UserBase, BaseSchema):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime


class UserResponsePublic(UserBase, BaseSchema):
    id: int
    created_at: datetime


class UserUpdateBase(BaseModel):
    username: str | None = Field(min_length=6, max_length=20, default=None)
    first_name: str | None = Field(min_length=2, max_length=20, default=None)
    last_name: str | None = Field(min_length=2, max_length=20, default=None)
    date_of_birth: Optional[date] = None
    address: str | None = Field(max_length=100, default=None)
    email: EmailStr | None = None

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, field: date) -> date:
        return validate_date_of_birth(field)
    
    @field_validator("email")
    @classmethod
    def valdiate_email(cls, field: str) -> str:
        return validate_email(field)


class UserUpdateAdmin(UserUpdateBase):
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserUpdateResponseAdmin(UserBase, BaseSchema):
    id: int
    role: UserRole
    is_active: bool
    updated_at: datetime


class UserUpdatePublic(UserUpdateBase):
    pass


class UserUpdateResponsePublic(UserBase, BaseSchema):
    id: int
    updated_at: datetime


class UserUpdatePasswordAdmin(BaseModel):
    new_password: str = Field(min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, field: str) -> str:
        return validate_password(field)
    

class UserUpdatePasswordPublic(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, field: str) -> str:
        return validate_password(field)


class UserSearch(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: Optional[date] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None