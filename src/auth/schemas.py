from pydantic import BaseModel, field_validator

from src.utils.schema_field_validator import validate_password


class LoginReponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class AccountActivationRequest(BaseModel):
    email: str
    invite_token: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, field: str) -> str:
        return validate_password(field)
    
class RefreshRequest(BaseModel):
    user_id: int
    refresh_token: str
    
class RefreshResponse(LoginReponse):
    pass