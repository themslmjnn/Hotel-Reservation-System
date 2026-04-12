from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User, UserRole
from src.users.schemas import SearchUserAdmin, SearchUserStaff


class UserRepositoryBase:
    @staticmethod
    def add_user(db: AsyncSession, new_user: User) -> None:
        db.add(new_user)

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
        query = (
            select(User)
            .filter(User.id == user_id)
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()


class UserRepositoryAdmin:
    @staticmethod
    async def get_all_users(db: AsyncSession) -> list[User]:
        query = select(User)

        result = await db.execute(query)

        return result.scalars().all()

    @staticmethod
    async def search_users(db: AsyncSession, search_request: SearchUserAdmin) -> list[User]:
        query = select(User)

        if search_request.username:
            query = query.filter(User.username.ilike('%' + search_request.username + '%'))

        if search_request.first_name:
            query = query.filter(User.first_name.ilike('%' + search_request.first_name + '%'))

        if search_request.last_name:
            query = query.filter(User.last_name.ilike('%' + search_request.last_name + '%'))

        if search_request.date_of_birth:
            query = query.filter(User.date_of_birth == search_request.date_of_birth)

        if search_request.email:
            query = query.filter(User.email.ilike('%' + search_request.email + '%'))

        if search_request.phone_number:
            query = query.filter(User.phone_number.ilike('%' + search_request.phone_number + '%'))

        if search_request.role:
            query = query.filter(User.role == search_request.role)

        if search_request.is_active is not None:
            query = query.filter(User.is_active == search_request.is_active)

        result = await db.execute(query)

        return result.scalars().all()
    

class UserRepositoryStaff:
    @staticmethod
    async def get_guests(db: AsyncSession) -> list[User]:
        query = (
            select(User)
            .filter(User.role == UserRole.guest)
        )

        result = await db.execute(query)

        return result.scalars().all()
    

    @staticmethod
    async def search_guests(db: AsyncSession, search_request: SearchUserStaff) -> list[User]:
        query = select(User)

        if search_request.username:
            query = query.filter(User.username.ilike('%' + search_request.username + '%'))

        if search_request.first_name:
            query = query.filter(User.first_name.ilike('%' + search_request.first_name + '%'))

        if search_request.last_name:
            query = query.filter(User.last_name.ilike('%' + search_request.last_name + '%'))

        if search_request.date_of_birth:
            query = query.filter(User.date_of_birth == search_request.date_of_birth)

        result = await db.execute(query)

        return result.scalars().all()