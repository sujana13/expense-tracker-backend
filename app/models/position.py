from sqlalchemy import Column, String, Boolean
from app.database.base import Base
import uuid

class Position(Base):
    __tablename__ = "positions"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )