from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ...core import security
from ...core.config import settings
from ... import crud
from ..deps import get_db, get_current_user
from ...schemas import user as user_schemas

router = APIRouter()

def create_access_token(subject: str) -> str:
    return security.create_access_token(subject=subject)

@router.post("/login")
async def login_access_token(username: str, password: str, db: Session = Depends(get_db)) -> Any:
    """OAuth2 compatible token login, get an access token for future requests."""
    user = crud.user.authenticate(db, username=username, password=password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(user.username)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/me", response_model=user_schemas.User)
async def read_users_me(request: Request) -> Any:
    """Get current user."""
    return request.state.user