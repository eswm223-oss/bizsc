from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User

#　selfはクラスのインスタンスメソッドとして使用するために必須の設定値、インスタンスで使用される

class UserRepository:
    def get_by_id(
        self,
        db: Session,
        user_id: int,
    ) -> User | None:
        statement = select(User).where(User.id == user_id)
        return db.scalar(statement)

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> User | None:
        statement = select(User).where(User.email == email)
        return db.scalar(statement)

    def get_all(
        self,
        db: Session,
        search: str,
        is_active: bool | None = None
    ) -> list[User]:
        statement = select(User)

        if search:
            statement = statement.where(
                User.email.like(f"%{search}%")
            )

        if is_active is not None:
            statement = statement.where(
                User.is_active == is_active
            )

        statement = statement.order_by(User.id)

        return list(db.scalars(statement).all())

    def create(
        self,
        db: Session,
        user: User,
    ) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(
        self,
        db: Session,
        user: User,
    ) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def delete(
        self,
        db: Session,
        user: User,
    ) -> None:
        db.delete(user)
        db.commit()