from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.user import RoleEnum


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.STUDENT

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "strongpassword123",
                "role": "STUDENT",
            }
        }
    )


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: RoleEnum
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None
    role: RoleEnum | None = None