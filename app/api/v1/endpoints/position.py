from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.position import (
    PositionCreate,
    PositionUpdate,
    PositionResponse,
)

from app.services.position_service import PositionService

router = APIRouter(
    prefix="/positions",
    tags=["Positions"],
)


@router.post(
    "",
    response_model=PositionResponse
)
def create_position(
    request: PositionCreate,
    db: Session = Depends(get_db)
):
    try:
        return PositionService.create(
            db,
            request
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "",
    response_model=list[PositionResponse]
)
def get_positions(
    db: Session = Depends(get_db)
):
    return PositionService.get_all(db)


@router.put(
    "/{position_id}",
    response_model=PositionResponse
)
def update_position(
    position_id: str,
    request: PositionUpdate,
    db: Session = Depends(get_db)
):
    try:
        return PositionService.update(
            db,
            position_id,
            request
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.delete(
    "/{position_id}"
)
def delete_position(
    position_id: str,
    db: Session = Depends(get_db)
):
    try:
        return PositionService.delete(
            db,
            position_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )