from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.category import Category
from app.models.user import UserRole
from app.schemas.category import CategoryCreate, CategoryOut
from app.core.permissions import require_roles
router=APIRouter()

@router.get("",response_model=list[CategoryOut])
def categories(db:Session=Depends(get_db), user=Depends(require_roles(UserRole.ADMIN,UserRole.SUPPORT_AGENT,UserRole.CUSTOMER))):
    return db.query(Category).filter(Category.is_active==True).all()

@router.post("",response_model=CategoryOut)
def create(data:CategoryCreate,db:Session=Depends(get_db),admin=Depends(require_roles(UserRole.ADMIN))):
    if db.query(Category).filter(Category.name==data.name).first(): raise HTTPException(409,"Category already exists")
    c=Category(name=data.name); db.add(c); db.commit(); db.refresh(c); return c

@router.put("/{category_id}",response_model=CategoryOut)
def update(category_id:int,data:CategoryCreate,db:Session=Depends(get_db),admin=Depends(require_roles(UserRole.ADMIN))):
    c=db.get(Category,category_id)
    if not c: raise HTTPException(404,"Category not found")
    c.name=data.name; db.commit(); db.refresh(c); return c

@router.patch("/{category_id}/activate",response_model=CategoryOut)
def activate(category_id:int,db:Session=Depends(get_db),admin=Depends(require_roles(UserRole.ADMIN))):
    c=db.get(Category,category_id)
    if not c: raise HTTPException(404,"Category not found")
    c.is_active=True; db.commit(); db.refresh(c); return c

@router.patch("/{category_id}/deactivate",response_model=CategoryOut)
def deactivate(category_id:int,db:Session=Depends(get_db),admin=Depends(require_roles(UserRole.ADMIN))):
    c=db.get(Category,category_id)
    if not c: raise HTTPException(404,"Category not found")
    c.is_active=False; db.commit(); db.refresh(c); return c
