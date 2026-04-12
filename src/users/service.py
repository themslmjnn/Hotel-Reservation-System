from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import generate_invite_token, hash_password, verify_password
from src.users.models import User, UserRole
from src.users.repository import (
    UserRepositoryAdmin,
    UserRepositoryBase,
    UserRepositoryStaff,
)
from src.users.schemas import (
    CreateUserAdmin,
    CreateUserGuest,
    CreateUserStaff,
    SearchUserAdmin,
    SearchUserStaff,
    UpdateUserAdmin,
    UpdateUserPasswordAdmin,
    UpdateUserPasswordPublic,
    UpdateUserPublic,
)
from src.utils.email import send_invite_email
from src.utils.exception_constants import HTTP400, HTTP404
from src.utils.exceptions import handle_user_integrity_error
from src.utils.helpers import ensure_exists, update_object


class UserServiceAdmin:
    @staticmethod
    async def create_user(db: AsyncSession, user_request: CreateUserAdmin, current_user: User) -> User:       
        if user_request.role == UserRole.system_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create system admin accounts through the API",
            ) 
        
        raw_invite_token, invite_token_hash = generate_invite_token()
        invite_token_expires_at = (
            datetime.now(timezone.utc) + timedelta(days=2)
        )

        new_user = User(\
            username=user_request.username,
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            date_of_birth=user_request.date_of_birth,
            email=user_request.email,
            phone_number=user_request.phone_number,
            role=user_request.role,
            is_active=False,
            invite_token_hash=invite_token_hash,
            invite_token_expires_at=invite_token_expires_at,
            created_by=current_user.id,
        )

        try:
            UserRepositoryBase.add_user(db, new_user)

            await db.commit()
            await db.refresh(new_user)

            send_invite_email(new_user.email, raw_invite_token)

            return new_user
        
        except IntegrityError as e:
            handle_user_integrity_error(e)
            raise


    @staticmethod
    async def get_all_users(db: AsyncSession) -> list[User]:
        users = await UserRepositoryAdmin.get_all_users(db)

        return users
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
        user = await UserRepositoryBase.get_user_by_id(db, user_id)

        ensure_exists(user, HTTP404.USER)

        return user
    
    @staticmethod
    async def search_users(db: AsyncSession, search_request: SearchUserAdmin) -> list[User]:
        users = await UserRepositoryAdmin.search_users(db, search_request)

        return users
    
    @staticmethod
    async def deactivate_user_by_id(db: AsyncSession, user_id: int) -> None:
        user = await UserRepositoryBase.get_user_by_id(db, user_id)

        ensure_exists(user, HTTP404.USER)
        
        user.is_active = False

        await db.commit()


    @staticmethod
    async def activate_account(db: AsyncSession, user_id: int) -> None:
        user = await UserRepositoryBase.get_user_by_id(db, user_id)

        ensure_exists(user, HTTP404.USER)
        
        user.is_active = True

        await db.commit()


    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, update_request: UpdateUserAdmin) -> User:
        user = await UserRepositoryBase.get_user_by_id(db, user_id)

        ensure_exists(user, HTTP404.USER)

        try:
            update_object(user, update_request)

            await db.commit()
            await db.refresh(user)

            return user
        
        except IntegrityError as e:
            handle_user_integrity_error(e)   
            raise


    @staticmethod
    async def update_password(db: AsyncSession, user_id: int, password_request: UpdateUserPasswordAdmin):
        user = await UserRepositoryBase.get_user_by_id(db, user_id)

        ensure_exists(user, HTTP404.USER)

        user.password_hash = hash_password(password_request.new_password)

        await db.commit()



class UserServiceStaff:
    @staticmethod
    async def create_guest(db: AsyncSession, guest_request: CreateUserStaff, current_user: User) -> User:
        raw_invite_token, invite_token_hash = generate_invite_token()
        invite_token_expires_at = (
            datetime.now(timezone.utc) + timedelta(days=2)
        )

        new_user = User(\
            username=guest_request.username,
            first_name=guest_request.first_name,
            last_name=guest_request.last_name,
            date_of_birth=guest_request.date_of_birth,
            email=guest_request.email,
            phone_number=guest_request.phone_number,
            role=UserRole.guest,
            is_active=False,
            invite_token_hash=invite_token_hash,
            invite_token_expires_at=invite_token_expires_at,
            created_by=current_user.id,
        )

        try:
            UserRepositoryBase.add_user(db, new_user)

            await db.commit()
            await db.refresh(new_user)

            send_invite_email(new_user.email, raw_invite_token)

            return new_user
        
        except IntegrityError as e:
            handle_user_integrity_error(e)
            raise


    @staticmethod
    async def get_guests(db: AsyncSession) -> list[User]:
        guests = await UserRepositoryStaff.get_guests(db)

        return guests
    

    @staticmethod
    async def search_guests(db: AsyncSession, search_request: SearchUserStaff) -> list[User]:
        guests = await UserRepositoryStaff.search_guests(db, search_request)

        return guests


class UserServiceGuest:
    @staticmethod
    async def create_account(db: AsyncSession, user_request: CreateUserGuest) -> User:
        new_user = User(\
            username=user_request.username,
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            date_of_birth=user_request.date_of_birth,
            email=user_request.email,
            phone_number=user_request.phone_number,
            password_hash=hash_password(user_request.password),
            role=UserRole.guest,
            is_active=True,
        )

        try:
            UserRepositoryBase.add_user(db, new_user)

            await db.commit()
            await db.refresh(new_user)

            return new_user
        
        except IntegrityError as e:
            handle_user_integrity_error(e)
            raise


    @staticmethod
    async def update_me(db: AsyncSession, update_request: UpdateUserPublic, current_user: User) -> User:
        try:
            update_object(current_user, update_request)

            await db.commit()
            await db.refresh(current_user)

            return current_user
        except IntegrityError as e:
            handle_user_integrity_error(e)
                
            raise


    @staticmethod
    async def update_my_password(db: AsyncSession, password_request: UpdateUserPasswordPublic, current_user: User) -> None:
        verify_password(password_request.old_password, current_user.password_hash, HTTP400.INCORRECT_PASSWORD)
        
        current_user.password_hash = hash_password(password_request.new_password)

        await db.commit()