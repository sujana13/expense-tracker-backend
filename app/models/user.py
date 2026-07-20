import uuid

from sqlalchemy import DateTime
from sqlalchemy import func

from app.database.base import Base

from sqlalchemy import Enum
from app.models.enums import UserRole

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Date,
)


class User(Base):
    __tablename__ = "users"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    hashed_password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(50),
        nullable=False,
        default=UserRole.EMPLOYEE.value
    )

    position = Column(
        String(100),
        nullable=True
)

    is_active = Column(
        Boolean,
        default=True
    )

    employee_id = Column(String(30), unique=True, nullable=True)

    phone = Column(String(20), nullable=True)

    gender = Column(String(20), nullable=True)

    location = Column(String(150), nullable=True)

    birth_date = Column(Date, nullable=True)

    date_of_joining = Column(Date, nullable=True)

    company_id = Column(
    String,
    ForeignKey("companies.id"),
    nullable=True
    )

    department_id = Column(
    String,
    ForeignKey("departments.id"),
    nullable=True
    )

    company = relationship(
    "Company",
    back_populates="users"
    )

    department = relationship(
    "Department",
    back_populates="users"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    
    