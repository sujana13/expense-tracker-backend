from sqlalchemy.orm import Session

from app.models.position import Position
from app.repositories.position_repository import PositionRepository
from app.schemas.position import (
    PositionCreate,
    PositionUpdate,
)


class PositionService:

    @staticmethod
    def create(db: Session, request: PositionCreate):

        existing = PositionRepository.get_by_name(
            db,
            request.name,
        )

        if existing:
            raise ValueError(
                "Position already exists"
            )

        position = Position(
            name=request.name
        )

        return PositionRepository.create(
            db,
            position
        )

    @staticmethod
    def get_all(db: Session):
        return PositionRepository.get_all(db)

    @staticmethod
    def update(
        db: Session,
        position_id: str,
        request: PositionUpdate,
    ):

        position = PositionRepository.get_by_id(
            db,
            position_id,
        )

        if not position:
            raise ValueError(
                "Position not found"
            )

        position.name = request.name
        position.is_active = request.is_active

        return PositionRepository.update(
            db,
            position,
        )

    @staticmethod
    def delete(
        db: Session,
        position_id: str,
    ):

        position = PositionRepository.get_by_id(
            db,
            position_id,
        )

        if not position:
            raise ValueError(
                "Position not found"
            )

        PositionRepository.delete(
            db,
            position,
        )

        return {
            "message": "Position deleted successfully"
        }