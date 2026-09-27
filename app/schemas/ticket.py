from datetime import datetime
from pydantic import BaseModel, Field
from app.models.ticket import Priority, TicketStatus
class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=1)
    category_id: int
    priority: Priority = Priority.MEDIUM
class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category_id: int | None = None
    priority: Priority | None = None
class StatusUpdate(BaseModel):
    status: TicketStatus
class AssignRequest(BaseModel):
    agent_id: int
class TicketOut(BaseModel):
    id: int
    ticket_number: str
    title: str
    description: str
    customer_id: int
    assigned_agent_id: int | None
    category_id: int
    priority: Priority
    status: TicketStatus
    due_date: datetime
    created_at: datetime
    updated_at: datetime | None = None
    model_config = {"from_attributes": True}
