from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models import User
from app.repositories import UserRepository
from app.schemas import UserCreate, UserUpdate
from app.core.exceptions import (
    EmailAlreadyRegisteredError,
    UserNotFoundError,
)

class UserService:
    def __init__(
        self,
        repository: UserRepository,
    ) -> None:
        self.repository = repository

    def create_user(
        self,
        db: Session,
        user_create: UserCreate,
    ) -> User:
        existing_user = self.repository.get_by_email(
            db,
            user_create.email,
        )

        if existing_user is not None:
            raise EmailAlreadyRegisteredError(
                "Email is already registered"
            )

        user = User(
            email=user_create.email,
            hashed_password=hash_password(user_create.password),
        )

        return self.repository.create(db, user)

    def get_user(
        self,
        db: Session,
        user_id: int,
    ) -> User:
        user = self.repository.get_by_id(db, user_id)

        if user is None:
            raise UserNotFoundError("User not found")

        return user

    def get_users(
        self,
        db: Session,
        search: str | None = None,
        is_active: bool | None = None,
        sort_by: str = "id",
        sort_order: str = "asc",
        page: int = 1,
        limit: int = 10,
    ) -> tuple[list[User], int]:
        
        users = self.repository.get_all(
            db, 
            search=search, 
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            limit=limit,
        )

        total = self.repository.count_all(
            db,
            search=search,
            is_active=is_active,
        )

        return users, total
    
    def update_user(
        self,
        db: Session,
        user_id: int,
        user_update: UserUpdate,
    ) -> User:

        user = self.get_user(db, user_id)
        #model_dumpはuser_updateをオブジェクトに変換する
        update_data = user_update.model_dump(exclude_unset=True)

        if "email" in update_data:
            existing_user = self.repository.get_by_email(
                db,
                update_data["email"],
            )

            if existing_user is not None:
                raise EmailAlreadyRegisteredError(
                    "Email is already registered"
                )

            user.email = update_data["email"]

        if "password" in update_data:
            user.hashed_password = hash_password(
                update_data["password"],
            )

        if "is_active" in update_data:
            user.is_active = update_data["is_active"]

        return self.repository.update(db, user)
    
    def delete_user(
        self,
        db: Session,
        user_id: int,
    ) -> None:
        user = self.get_user(db, user_id)
        self.repository.delete(db, user)