from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str


class CompanyUpdate(BaseModel):
    name: str
    is_active: bool


class CompanyResponse(BaseModel):
    id: str
    name: str
    is_active: bool

    class Config:
        from_attributes = True