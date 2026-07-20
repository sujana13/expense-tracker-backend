from pydantic import BaseModel


class PositionCreate(BaseModel):
    name: str


class PositionUpdate(BaseModel):
    name: str
    is_active: bool


class PositionResponse(BaseModel):
    id: str
    name: str
    is_active: bool

    class Config:
        from_attributes = True