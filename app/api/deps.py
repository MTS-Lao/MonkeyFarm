from typing import Generator, Optional
from fastapi import Request, HTTPException, status
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..core import security
from ..core.config import settings
from ..database import SessionLocal
from ..models import User

class TokenData(BaseModel):
    username: Optional[str] = None

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_token_from_cookie(request: Request) -> Optional[str]:
    authorization = request.cookies.get("access_token")
    if not authorization:
        return None
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        return token
    except ValueError:
        return None

async def get_current_user_optional(
    request: Request,
    db: Session = None
) -> Optional[User]:
    if db is None:
        db = next(get_db())
    
    token = get_token_from_cookie(request)
    if not token:
        return None
        
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except JWTError:
        return None
    
    user = db.query(User).filter(User.username == token_data.username).first()
    return user

async def get_current_user(
    request: Request,
    db: Session = None
) -> User:
    user = await get_current_user_optional(request, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_current_active_admin(
    current_user: User = None,
) -> User:
    if not current_user or not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user

def check_admin_access(current_user: User = None):
    if not current_user or not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to perform this action"
        )
    return current_user