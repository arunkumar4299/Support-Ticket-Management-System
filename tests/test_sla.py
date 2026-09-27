from datetime import datetime, timezone
from app.services.sla_service import calculate_due_date
from app.models.ticket import Priority
def test_critical_sla():
    start=datetime(2026,1,1,tzinfo=timezone.utc)
    assert (calculate_due_date(Priority.CRITICAL,start)-start).total_seconds()==4*3600
