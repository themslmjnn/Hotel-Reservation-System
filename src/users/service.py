from sqlalchemy.ext.asyncio import AsyncSession

from users.schemas import UserCreateAdmin, UserSearch, UserUpdateAdmin, UserUpdatePasswordPublic, UserUpdatePasswordAdmin
from src.users.models import User
from src.core.security import hash_password, verify_password
from src.users.repository import UserRepository
from sqlalchemy.exc import IntegrityError
from src.utils.exceptions import check_unique_email_error, check_unique_username_error
from src.utils.helpers import update_object, ensure_exists
from src.utils.exception_constants import MESSAGE_404_USER, MESSAGE_400_PASSWORD

class UserServiceAdmin:
    @staticmethod
    async def create_user(db: AsyncSession, user_request: UserCreateAdmin) -> User:
        new_user = User(\
            username=user_request.username,
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            date_of_birth=user_request.date_of_birth,
            address=user_request.address,
            email_address=user_request.email_address,
            password_hash=hash_password(user_request.password),
            role=user_request.role,
            is_active=True
        )

        try:
            UserRepository.add_user(db, new_user)

            await db.commit()
            await db.refresh(new_user)

            return new_user
        
        except IntegrityError as e:
            check_unique_username_error(e)
            check_unique_email_error(e)
                
            raise

    @staticmethod
    async def get_all_users(db: AsyncSession) -> list[User]:
        users = await UserRepository.get_all_users(db)

        return users
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
        user = await UserRepository.get_user_by_id(db, user_id)

        ensure_exists(user, MESSAGE_404_USER)

        return user
    
    @staticmethod
    async def search_users(db: AsyncSession, search_request: UserSearch) -> list[User]:
        users = await UserRepository.search_users(db, search_request)

        return users
    
    @staticmethod
    async def deactivate_user_by_id(db: AsyncSession, user_id: int) -> None:
        user = await UserRepository.get_user_by_id(db, user_id)

        ensure_exists(user, MESSAGE_404_USER)
        
        user.is_active = False

        await db.commit()


    @staticmethod
    async def activate_account(db: AsyncSession, user_id: int) -> None:
        user = await UserRepository.get_user_by_id(db, user_id)

        ensure_exists(user, MESSAGE_404_USER)
        
        user.is_active = True

        await db.commit()


    @staticmethod
    async def update_user(db: AsyncSession, update_request: UserUpdateAdmin, user_id: int) -> User:
        user = await UserRepository.get_user_by_id(db, user_id)

        ensure_exists(user, MESSAGE_404_USER)

        try:
            update_object(user, update_request)

            await db.commit()
            await db.refresh(user)

            return user
        
        except IntegrityError as e:
            check_unique_username_error(e)
            check_unique_email_error(e)
                
            raise


    @staticmethod
    async def update_password(db: AsyncSession, user_id: int, password_request: UserUpdatePasswordAdmin):
        user = await UserRepository.get_user_by_id(db, user_id)

        ensure_exists(user, MESSAGE_404_USER)

        user.password_hash = hash_password(password_request.new_password)

        await db.commit()


class UserServicePublic:
    @staticmethod
    async def update_me(db: AsyncSession, current_user: User, update_request: UserUpdateAdmin) -> User:
        try:
            update_object(current_user, update_request)

            await db.commit()
            await db.refresh(current_user)

            return current_user
        except IntegrityError as e:
            check_unique_username_error(e)
            check_unique_email_error(e)
                
            raise


    @staticmethod
    async def update_my_password(db: AsyncSession, current_user: User, password_request: UserUpdatePasswordPublic) -> None:
        verify_password(password_request.old_password, current_user.password_hash, MESSAGE_400_PASSWORD)
        
        current_user.password_hash = hash_password(password_request.new_password)

        await db.commit()