from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str


class DepartmentUpdate(BaseModel):
    name: str
    is_active: bool


class DepartmentResponse(BaseModel):
    id: str
    name: str
    is_active: bool

    class Config:
        from_attributes = True