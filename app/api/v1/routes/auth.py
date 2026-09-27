from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, ChangePasswordRequest
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.permissions import get_current_user
router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(409, "Email already registered")
    user = User(name=data.name, email=data.email, password_hash=hash_password(data.password))
    db.add(user); db.commit(); db.refresh(user)
    access = create_access_token(str(user.id)); refresh = create_refresh_token(str(user.id))
    db.add(RefreshToken(user_id=user.id, token=refresh, expires_at=datetime.now(timezone.utc)+timedelta(days=7)))
    db.commit()
    return {"access_token": access, "refresh_token": refresh}

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    if not user.is_active:
        raise HTTPException(401, "Inactive user cannot authenticate")
    access = create_access_token(str(user.id)); refresh = create_refresh_token(str(user.id))
    db.add(RefreshToken(user_id=user.id, token=refresh, expires_at=datetime.now(timezone.utc)+timedelta(days=7)))
    db.commit()
    return {"access_token": access, "refresh_token": refresh}

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = decode_token(refresh_token)
    stored = db.query(RefreshToken).filter(RefreshToken.token == refresh_token, RefreshToken.revoked == False).first()
    if not payload or payload.get("type") != "refresh" or not stored:
        raise HTTPException(401, "Invalid refresh token")
    access = create_access_token(payload["sub"])
    return {"access_token": access, "refresh_token": refresh_token}

@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    stored = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if stored: stored.revoked = True; db.commit()
    return {"success": True, "message": "Logged out"}

@router.get("/me")
def me(user=Depends(get_current_user)):
    return {"success": True, "data": {"id": user.id, "name": user.name, "email": user.email, "role": user.role, "is_active": user.is_active}}

@router.post("/change-password")
def change_password(data: ChangePasswordRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(data.current_password, user.password_hash):
        raise HTTPException(400, "Current password is incorrect")
    user.password_hash = hash_password(data.new_password); db.commit()
    return {"success": True, "message": "Password changed"}
