import secrets
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core.config import settings
from src.utils.exception_constants import MESSAGE_TOKEN_ERR


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(payload: dict) -> str:
    data = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})

    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
    except JWTError:
        raise ValueError(MESSAGE_TOKEN_ERR)
    

def generate_invite_token() -> tuple[str, str]:
    raw_token = secrets.token_urlsafe(32)
    hashed_token = pwd_context.hash(raw_token)

    return raw_token, hashed_token


def verify_invite_token(raw_token: str, hashed_token: str) -> bool:
    return pwd_context.verify(raw_token, hashed_token)


def generate_refresh_token() -> tuple[str, str]:
    raw_token = secrets.token_urlsafe(32)
    hashed_token = pwd_context.hash(raw_token)
    return raw_token, hashed_token


def verify_refresh_token(raw_token: str, hashed_token: str) -> bool:
    return pwd_context.verify(raw_token, hashed_token)