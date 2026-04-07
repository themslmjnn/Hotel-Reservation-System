from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User


class UserRepository:
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int):
        query = (
            select(User)
            .filter(User.id == user_id)
        )

        result = await db.execute(query)

        return result.scalars().first()