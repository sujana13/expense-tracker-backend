from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str
    description: str | None = None
    is_active: bool


class CategoryResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    is_active: bool

    model_config = {
        "from_attributes": True
    }