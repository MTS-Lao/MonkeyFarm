from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from ...crud import user as crud_user
from ...schemas import user as user_schemas
from ...api import deps
from ...core import security

router = APIRouter()

@router.get("/", response_model=List[user_schemas.User])
def get_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve users.
    """
    return crud_user.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=user_schemas.User)
@router.post("", response_model=user_schemas.User)
def create_user(
    db: Session = Depends(deps.get_db),
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    phone: Optional[str] = Form(None),
    is_admin: bool = Form(False)
):
    """Create new user."""
    try:
        if password != confirm_password:
            raise HTTPException(
                status_code=400,
                detail="Passwords do not match"
            )

        existing_user = crud_user.get_by_username(db, username=username)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Username already registered"
            )

        user_in = user_schemas.UserCreate(
            username=username,
            password=password,
            confirm_password=confirm_password,
            phone=phone,
            is_admin=is_admin
        )
        return crud_user.create(db, obj_in=user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=user_schemas.User)
def get_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Get user by ID.
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Convert to dict with explicit datetime values
    user_data = {
        "id": user.id,
        "username": user.username,
        "phone": user.phone,
        "is_admin": user.is_admin,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
    return user_data

@router.put("/{user_id}", response_model=user_schemas.User)
def update_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    username: str = Form(...),
    password: Optional[str] = Form(None),
    confirm_password: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    is_admin: bool = Form(False)
):
    """Update user."""
    try:
        print(f"Updating user {user_id} with password: {bool(password)}")  # Debug log
        
        user = crud_user.get(db, id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if username is taken by another user
        existing_user = crud_user.get_by_username(db, username=username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=400,
                detail="Username already registered"
            )

        update_data = {
            "username": username,
            "phone": phone,
            "is_admin": is_admin
        }

        # Handle password update
        if password:
            if not confirm_password:
                raise HTTPException(
                    status_code=400,
                    detail="Confirm password is required when updating password"
                )
            if password != confirm_password:
                raise HTTPException(
                    status_code=400,
                    detail="Passwords do not match"
                )
            update_data["password"] = password
            print("Password will be updated")  # Debug log

        # Update user
        try:
            updated_user = crud_user.update(db, db_obj=user, obj_in=update_data)
            print(f"User updated successfully: {updated_user.username}")  # Debug log
            return updated_user
        except Exception as e:
            print(f"Error updating user: {str(e)}")  # Debug log
            raise HTTPException(
                status_code=500,
                detail=f"Error updating user: {str(e)}"
            )

    except ValueError as e:
        print(f"Validation error: {str(e)}")  # Debug log
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debug log
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error occurred: {str(e)}"
        )
    
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Delete user.
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud_user.remove(db, id=user_id)
    return {"status": "success"}
