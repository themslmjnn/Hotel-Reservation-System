from src.database import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


db_dependency = Annotated[AsyncSession, Depends(get_db)]