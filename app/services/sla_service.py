from datetime import datetime, timedelta, timezone
from app.models.ticket import Priority
SLA_HOURS = {
    Priority.LOW: 72,
    Priority.MEDIUM: 48,
    Priority.HIGH: 24,
    Priority.CRITICAL: 4,
}
def calculate_due_date(priority: Priority, created_at: datetime | None = None):
    created_at = created_at or datetime.now(timezone.utc)
    return created_at + timedelta(hours=SLA_HOURS[priority])
def is_overdue(due_date: datetime) -> bool:
    return datetime.now(timezone.utc) > due_date
