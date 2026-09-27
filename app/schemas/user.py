from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.CUSTOMER
class UserUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None
    model_config = {"from_attributes": True}
