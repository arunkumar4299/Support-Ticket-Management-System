from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.core.permissions import require_roles
from app.core.security import hash_password
router = APIRouter()

@router.post("", response_model=UserOut)
def create_user(data: UserCreate, db: Session = Depends(get_db), admin=Depends(require_roles(UserRole.ADMIN))):
    if db.query(User).filter(User.email == data.email).first(): raise HTTPException(409, "Email already exists")
    user = User(name=data.name, email=data.email, password_hash=hash_password(data.password), role=data.role)
    db.add(user); db.commit(); db.refresh(user); return user

@router.get("", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db), admin=Depends(require_roles(UserRole.ADMIN))):
    return db.query(User).order_by(User.id.desc()).all()

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), admin=Depends(require_roles(UserRole.ADMIN))):
    user = db.get(User, user_id)
    if not user: raise HTTPException(404, "User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), admin=Depends(require_roles(UserRole.ADMIN))):
    user = db.get(User, user_id)
    if not user: raise HTTPException(404, "User not found")
    for key, value in data.model_dump(exclude_unset=True).items(): setattr(user, key, value)
    db.commit(); db.refresh(user); return user

@router.patch("/{user_id}/role", response_model=UserOut)
def change_role(user_id: int, role: UserRole, db: Session = Depends(get_db), admin=Depends(require_roles(UserRole.ADMIN))):
    user = db.get(User, user_id)
    if not user: raise HTTPException(404, "User not found")
    user.role = role; db.commit(); db.refresh(user); return user

@router.patch("/{user_id}/activate", response_model=UserOut)
def activate(user_id: int, db: Session = Depends(get_db), admin=Depends(require_roles(UserRole.ADMIN))):
    user=db.get(User,user_id)
    if not user: raise HTTPException(404,"User not found")
    user.is_active=True; db.commit(); db.refresh(user); return user

@router.patch("/{user_id}/deactivate", response_model=UserOut)
def deactivate(user_id: int, db: Session = Depends(get_db), admin=Depends(require_roles(UserRole.ADMIN))):
    user=db.get(User,user_id)
    if not user: raise HTTPException(404,"User not found")
    user.is_active=False; db.commit(); db.refresh(user); return user
