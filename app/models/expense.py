import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import func

from app.database.base import Base

from sqlalchemy import Enum
from app.models.enums import ExpenseStatus
from sqlalchemy.orm import relationship


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

    status = Column(
        Enum(ExpenseStatus),
        nullable=False,
        default=ExpenseStatus.SUBMITTED
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

    receipt_path = Column(
        String,
        nullable=True
    )

    approved_by = Column(
        String,
        ForeignKey("users.id"),
        nullable=True
    )

    approved_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    rejected_by = Column(
        String,
        ForeignKey("users.id"),
        nullable=True
    )

    rejected_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    rejection_reason = Column(
        String(500),
        nullable=True
    )

    paid_by = Column(
        String,
        ForeignKey("users.id"),
        nullable=True
    )

    paid_at = Column(
        DateTime(timezone=True),
        nullable=True
)

    payment_reference = Column(
        String(200),
        nullable=True
    )

    payment_notes = Column(
        String(500),
        nullable=True
)    

    approved_by_user = relationship(
       "User",
       foreign_keys=[approved_by],
)

    rejected_by_user = relationship(
        "User",
        foreign_keys=[rejected_by],
)
    paid_by_user = relationship(
        "User",
        foreign_keys=[paid_by]
)

    submitted_by_user = relationship(
        "User",
        foreign_keys=[user_id]
)

    category = relationship(
       "Category",
       foreign_keys=[category_id]
)

    @property
    def approved_by_name(self):
        return (
            self.approved_by_user.username
            if self.approved_by_user
            else None
        )


    @property
    def rejected_by_name(self):
        return (
            self.rejected_by_user.username
            if self.rejected_by_user
            else None
        )


    @property
    def paid_by_name(self):
        return (
            self.paid_by_user.username
            if self.paid_by_user
            else None
        )
     

    @property
    def submitted_by_name(self):
        return (
            self.submitted_by_user.username
            if self.submitted_by_user
            else None
    )
    
    @property
    def category_name(self):
        return (
           self.category.name
           if self.category
           else None
        )