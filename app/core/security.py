from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password[:72], hashed)

def create_token(subject: str, token_type: str, expires_delta: timedelta):
    now = datetime.now(timezone.utc)
    payload = {"sub": subject, "type": token_type, "iat": now, "exp": now + expires_delta}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def create_access_token(subject: str):
    return create_token(subject, "access", timedelta(minutes=settings.access_token_expire_minutes))

def create_refresh_token(subject: str):
    return create_token(subject, "refresh", timedelta(days=settings.refresh_token_expire_days))

def decode_token(token: str):
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return None
