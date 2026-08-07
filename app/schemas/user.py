from pydantic import BaseModel, EmailStr, Field

from app.models.enums import UserRole

from pydantic import ConfigDict
from datetime import date
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Date,
)




class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)
    role: UserRole = UserRole.EMPLOYEE
    position: str | None = None

    employee_id: str | None = None
    phone: str | None = None
    gender: str | None = None
    location: str | None = None
    birth_date: date | None = None
    date_of_joining: date | None = None

class UserUpdate(BaseModel):
    username: str
    role: UserRole
    is_active: bool

    company_id: str | None = None
    department_id: str | None = None
    position: str | None = None
    employee_id: str | None = None
    phone: str | None = None
    gender: str | None = None
    location: str | None = None
    birth_date: date | None = None
    date_of_joining: date | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    email: EmailStr
    role: str
    is_active: bool

    company_id: str | None = None
    department_id: str | None = None

    company_name: str | None = None
    department_name: str | None = None
    position: str | None = None

    employee_id: str | None = None
    phone: str | None = None
    gender: str | None = None
    location: str | None = None
    birth_date: date | None = None
    date_of_joining: date | None = None
    profile_picture: str | None = None

    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(
        min_length=8,
        max_length=50
    )
