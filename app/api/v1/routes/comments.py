from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.comment import Comment
from app.models.ticket import TicketStatus
from app.schemas.comment import CommentCreate, CommentOut
from app.core.permissions import get_current_user
router=APIRouter()

@router.post("/{ticket_id}/comments",response_model=CommentOut)
def add_comment(ticket_id:int,data:CommentCreate,db:Session=Depends(get_db),user=Depends(get_current_user)):
    ticket=db.get(__import__('app.models.ticket',fromlist=['Ticket']).Ticket,ticket_id)
    if not ticket: raise HTTPException(404,"Ticket not found")
    if ticket.status==TicketStatus.CLOSED: raise HTTPException(400,"Closed tickets cannot receive comments")
    c=Comment(ticket_id=ticket_id,user_id=user.id,message=data.message); db.add(c); db.commit(); db.refresh(c); return c

@router.get("/{ticket_id}/comments",response_model=list[CommentOut])
def list_comments(ticket_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    return db.query(Comment).filter(Comment.ticket_id==ticket_id).order_by(Comment.created_at).all()

@router.put("/comments/{comment_id}",response_model=CommentOut)
def update_comment(comment_id:int,data:CommentCreate,db:Session=Depends(get_db),user=Depends(get_current_user)):
    c=db.get(Comment,comment_id)
    if not c: raise HTTPException(404,"Comment not found")
    if c.user_id!=user.id and user.role.value!="admin": raise HTTPException(403,"You can only edit your own comment")
    c.message=data.message; db.commit(); db.refresh(c); return c

@router.delete("/comments/{comment_id}")
def delete_comment(comment_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    c=db.get(Comment,comment_id)
    if not c: raise HTTPException(404,"Comment not found")
    if c.user_id!=user.id and user.role.value!="admin": raise HTTPException(403,"You can only delete your own comment")
    db.delete(c); db.commit(); return {"success":True}
