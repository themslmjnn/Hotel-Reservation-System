from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User
from src.users.schemas import UserSearch


class UserRepository:
    @staticmethod
    async def add_user(db: AsyncSession, new_user: User) -> None:
        await db.add(new_user)

    @staticmethod
    async def get_all_users(db: AsyncSession) -> list[User]:
        query = select(User)

        result = await db.execute(query)

        return result.scalars().all()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
        query = (
            select(User)
            .filter(User.id == user_id)
        )

        result = await db.execute(query)

        return result.scalars().first()

    @staticmethod
    async def search_users(db: AsyncSession, search_request: UserSearch) -> list[User]:
        query = select(User)

        if search_request.username:
            query = query.filter(User.username.ilike('%' + search_request.username + '%'))

        if search_request.first_name:
            query = query.filter(User.first_name.ilike('%' + search_request.first_name + '%'))

        if search_request.last_name:
            query = query.filter(User.last_name.ilike('%' + search_request.last_name + '%'))

        if search_request.date_of_birth:
            query = query.filter(User.date_of_birth == search_request.date_of_birth)

        if search_request.role:
            query = query.filter(User.role == search_request.role)

        if search_request.is_active is not None:
            query = query.filter(User.is_active == search_request.is_active)

        result = await db.execute(query)

        return result.scalars().all()