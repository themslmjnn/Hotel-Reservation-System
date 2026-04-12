from pydantic import EmailStr
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User
from src.users.schemas import UserSearchAdmin


class UserRepository:
    @staticmethod
    def add_user(db: AsyncSession, new_user: User) -> None:
        db.add(new_user)

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

        return result.scalar_one_or_none()

    @staticmethod
    async def search_users_admin(db: AsyncSession, search_request: UserSearchAdmin) -> list[User]:
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
    

    @staticmethod
    async def email_exists(db: AsyncSession, email: EmailStr) -> bool:
        query = (
            select(exists().filter(User.email == email))
        )

        result = await db.execute(query)

        return result.scalar()
    
    @staticmethod
    async def phone_number_exists(db: AsyncSession, phone_number: str) -> bool:
        query = (
            select(exists().filter(User.phone_number == phone_number))
        )

        result = await db.execute(query)

        return result.scalar()
    
    @staticmethod
    async def username_exists(db: AsyncSession, username: str) -> bool:
        query = (
            select(exists().filter(User.username == username))
        )

        result = await db.execute(query)

        return result.scalar()