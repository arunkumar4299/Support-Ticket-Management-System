from pydantic import BaseModel
class CategoryCreate(BaseModel):
    name: str
class CategoryOut(BaseModel):
    id: int
    name: str
    is_active: bool
    model_config = {"from_attributes": True}
