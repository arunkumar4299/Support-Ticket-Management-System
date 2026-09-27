from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.database import get_db
from app.models.ticket import Ticket, TicketStatus, Priority
from app.models.category import Category
from app.models.user import User, UserRole
from app.models.status_history import TicketStatusHistory
from app.schemas.ticket import TicketCreate, TicketUpdate, StatusUpdate, AssignRequest, TicketOut
from app.core.permissions import get_current_user, require_roles
from app.services.sla_service import calculate_due_date
router=APIRouter()

ALLOWED = {
    TicketStatus.OPEN: {TicketStatus.IN_PROGRESS},
    TicketStatus.IN_PROGRESS: {TicketStatus.RESOLVED},
    TicketStatus.RESOLVED: {TicketStatus.IN_PROGRESS, TicketStatus.CLOSED},
    TicketStatus.CLOSED: set(),
}

def accessible(ticket, user):
    return user.role == UserRole.ADMIN or ticket.customer_id == user.id or ticket.assigned_agent_id == user.id

@router.post("", response_model=TicketOut)
def create_ticket(data: TicketCreate, db: Session=Depends(get_db), user=Depends(get_current_user)):
    category=db.get(Category,data.category_id)
    if not category or not category.is_active: raise HTTPException(400,"Invalid or inactive category")
    ticket=Ticket(ticket_number=f"TKT-{uuid4().hex[:10].upper()}", title=data.title, description=data.description,
                  customer_id=user.id, category_id=data.category_id, priority=data.priority,
                  due_date=calculate_due_date(data.priority))
    db.add(ticket); db.commit(); db.refresh(ticket); return ticket

@router.get("", response_model=list[TicketOut])
def list_tickets(page:int=Query(1,ge=1), page_size:int=Query(20,ge=1,le=100),
                 search:str|None=None, status:TicketStatus|None=None, priority:Priority|None=None,
                 category_id:int|None=None, assigned_agent_id:int|None=None,
                 db:Session=Depends(get_db), user=Depends(get_current_user)):
    q=db.query(Ticket)
    if user.role == UserRole.CUSTOMER: q=q.filter(Ticket.customer_id==user.id)
    elif user.role == UserRole.SUPPORT_AGENT: q=q.filter(or_(Ticket.assigned_agent_id==user.id, Ticket.assigned_agent_id==None))
    if search: q=q.filter(or_(Ticket.title.ilike(f"%{search}%"),Ticket.description.ilike(f"%{search}%"),Ticket.ticket_number.ilike(f"%{search}%")))
    if status: q=q.filter(Ticket.status==status)
    if priority: q=q.filter(Ticket.priority==priority)
    if category_id: q=q.filter(Ticket.category_id==category_id)
    if assigned_agent_id: q=q.filter(Ticket.assigned_agent_id==assigned_agent_id)
    return q.order_by(Ticket.created_at.desc()).offset((page-1)*page_size).limit(page_size).all()

@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    ticket=db.get(Ticket,ticket_id)
    if not ticket or not accessible(ticket,user): raise HTTPException(404,"Ticket not found")
    return ticket

@router.put("/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id:int,data:TicketUpdate,db:Session=Depends(get_db),user=Depends(get_current_user)):
    ticket=db.get(Ticket,ticket_id)
    if not ticket or not accessible(ticket,user): raise HTTPException(404,"Ticket not found")
    if ticket.status == TicketStatus.CLOSED: raise HTTPException(400,"Closed tickets cannot be modified")
    for k,v in data.model_dump(exclude_unset=True).items():
        if k=="category_id":
            c=db.get(Category,v)
            if not c or not c.is_active: raise HTTPException(400,"Invalid or inactive category")
        setattr(ticket,k,v)
    if data.priority: ticket.due_date=calculate_due_date(data.priority)
    db.commit(); db.refresh(ticket); return ticket

@router.patch("/{ticket_id}/status", response_model=TicketOut)
def update_status(ticket_id:int,data:StatusUpdate,db:Session=Depends(get_db),user=Depends(get_current_user)):
    ticket=db.get(Ticket,ticket_id)
    if not ticket or not accessible(ticket,user): raise HTTPException(404,"Ticket not found")
    if data.status not in ALLOWED[ticket.status]: raise HTTPException(400,detail=f"Invalid status transition: {ticket.status} -> {data.status}")
    old=ticket.status; ticket.status=data.status
    db.add(TicketStatusHistory(ticket_id=ticket.id,changed_by=user.id,old_status=old.value,new_status=data.status.value))
    db.commit(); db.refresh(ticket); return ticket

@router.patch("/{ticket_id}/assign", response_model=TicketOut)
def assign_ticket(ticket_id:int,data:AssignRequest,db:Session=Depends(get_db),admin=Depends(require_roles(UserRole.ADMIN,UserRole.SUPPORT_AGENT))):
    ticket=db.get(Ticket,ticket_id)
    agent=db.get(User,data.agent_id)
    if not ticket: raise HTTPException(404,"Ticket not found")
    if not agent or agent.role != UserRole.SUPPORT_AGENT or not agent.is_active: raise HTTPException(400,"Inactive or invalid support agent")
    ticket.assigned_agent_id=agent.id; db.commit(); db.refresh(ticket); return ticket

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id:int,db:Session=Depends(get_db),admin=Depends(require_roles(UserRole.ADMIN))):
    ticket=db.get(Ticket,ticket_id)
    if not ticket: raise HTTPException(404,"Ticket not found")
    db.delete(ticket); db.commit(); return {"success":True,"message":"Ticket deleted"}
