import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import func

from app.database.base import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    expense_date = Column(
        Date,
        nullable=False
    )

    payment_method = Column(
        String(50),
        nullable=False
    )

    category_id = Column(
        String,
        ForeignKey("categories.id"),
        nullable=False
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False
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