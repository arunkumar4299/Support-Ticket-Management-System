from datetime import datetime
from pydantic import BaseModel, Field
class CommentCreate(BaseModel):
    message: str = Field(min_length=1)
class CommentOut(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    message: str
    created_at: datetime
    updated_at: datetime | None = None
    model_config = {"from_attributes": True}
