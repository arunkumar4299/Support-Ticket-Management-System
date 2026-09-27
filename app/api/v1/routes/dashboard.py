from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.ticket import Ticket, TicketStatus, Priority
from app.models.user import User, UserRole
from app.core.permissions import get_current_user
from app.services.sla_service import is_overdue
router=APIRouter()

@router.get("")
def dashboard(db:Session=Depends(get_db),user=Depends(get_current_user)):
    q=db.query(Ticket)
    if user.role==UserRole.CUSTOMER: q=q.filter(Ticket.customer_id==user.id)
    if user.role==UserRole.SUPPORT_AGENT: q=q.filter(Ticket.assigned_agent_id==user.id)
    tickets=q.all()
    result={
        "total_tickets":len(tickets),
        "open_tickets":sum(t.status==TicketStatus.OPEN for t in tickets),
        "in_progress_tickets":sum(t.status==TicketStatus.IN_PROGRESS for t in tickets),
        "resolved_tickets":sum(t.status==TicketStatus.RESOLVED for t in tickets),
        "closed_tickets":sum(t.status==TicketStatus.CLOSED for t in tickets),
        "overdue_tickets":sum(is_overdue(t.due_date) and t.status!=TicketStatus.CLOSED for t in tickets),
        "critical_tickets":sum(t.priority==Priority.CRITICAL for t in tickets),
    }
    if user.role==UserRole.ADMIN:
        result.update({
            "total_customers":db.query(User).filter(User.role==UserRole.CUSTOMER).count(),
            "total_agents":db.query(User).filter(User.role==UserRole.SUPPORT_AGENT).count(),
            "active_agents":db.query(User).filter(User.role==UserRole.SUPPORT_AGENT,User.is_active==True).count(),
        })
    return result
