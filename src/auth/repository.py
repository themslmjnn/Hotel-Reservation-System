from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User


class AuthRepository:
    @staticmethod
    async def get_by_login_identifier(db: AsyncSession, identifier: str) -> User | None:
        query = (
            select(User)
            .filter(or_(
                User.username == identifier,
                User.phone_number == identifier,
                User.email == identifier
            ))
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()
    

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
        query = (
            select(User)
            .filter(User.id == user_id)
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()