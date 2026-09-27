from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Index
from app.db.database import Base
import enum

class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    ticket_number = Column(String(30), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    assigned_agent_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    category_id = Column(Integer, ForeignKey("ticket_categories.id"), nullable=False, index=True)
    priority = Column(Enum(Priority), default=Priority.MEDIUM, nullable=False, index=True)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False, index=True)
    due_date = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    __table_args__ = (Index("ix_ticket_status_priority", "status", "priority"),)
