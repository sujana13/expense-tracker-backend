from sqlalchemy.orm import Session
from app.models.position import Position


class PositionRepository:

    @staticmethod
    def create(db: Session, position: Position):
        db.add(position)
        db.commit()
        db.refresh(position)
        return position

    @staticmethod
    def get_all(db: Session):
        return db.query(Position).all()

    @staticmethod
    def get_by_id(db: Session, position_id: str):
        return (
            db.query(Position)
            .filter(Position.id == position_id)
            .first()
        )

    @staticmethod
    def get_by_name(db: Session, name: str):
        return (
            db.query(Position)
            .filter(Position.name == name)
            .first()
        )

    @staticmethod
    def update(db: Session, position: Position):
        db.commit()
        db.refresh(position)
        return position

    @staticmethod
    def delete(db: Session, position: Position):
        db.delete(position)
        db.commit()