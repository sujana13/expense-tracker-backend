from pydantic import BaseModel, EmailStr, Field

from app.enums.role import UserRole


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)
    role: UserRole = UserRole.EMPLOYEE


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True