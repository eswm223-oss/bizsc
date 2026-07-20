from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories import UserRepository
from app.schemas import (
    UserCreate, 
    UserResponse, 
    UserListResponse,
    UserUpdate,
)

from app.services import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

user_service = UserService(UserRepository())


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    user = user_service.create_user(db, user_create)
    return UserResponse.model_validate(user)


@router.get(
    "",
    response_model=UserListResponse,
)
def get_users(
    db: Session = Depends(get_db),
) -> UserListResponse:
    users = user_service.get_users(db)

    return UserListResponse(
        users=[
            UserResponse.model_validate(user)
            for user in users
        ],
        total=len(users),
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> UserResponse:
    user = user_service.get_user(db, user_id)
    return UserResponse.model_validate(user)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
) -> UserResponse:
    user = user_service.update_user(
        db,
        user_id,
        user_update,
    )

    return UserResponse.model_validate(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> None:
    user_service.delete_user(db, user_id)