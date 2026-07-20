from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
    )


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(
        default=None,
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
    )
    is_active: bool | None = None

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "UserUpdate":
        if (
            self.email is None
            and self.password is None
            and self.is_active is None
        ):
            raise ValueError(
                "At least one field must be provided"
            )

        return self


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int