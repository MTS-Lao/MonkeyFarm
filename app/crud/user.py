from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from ..core.security import get_password_hash, verify_password
from ..models import User
from ..schemas.user import UserCreate, UserUpdate

def get(db: Session, id: int) -> Optional[User]:
    return db.query(User).filter(User.id == id).first()

def get_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_multi(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: UserCreate) -> User:
    hashed_password = get_password_hash(obj_in.password)
    db_obj = User(
        username=obj_in.username,
        password=hashed_password,
        phone=obj_in.phone,
        is_admin=obj_in.is_admin
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session,
    *,
    db_obj: User,
    obj_in: Union[UserUpdate, Dict[str, Any]]
) -> User:
    try:
        update_data = obj_in.dict() if not isinstance(obj_in, dict) else obj_in
        
        # Handle password update
        if "password" in update_data and update_data["password"]:
            print("Hashing new password")  # Debug log
            hashed_password = get_password_hash(update_data["password"])
            update_data["password"] = hashed_password

        for field in ['username', 'phone', 'is_admin', 'password']:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception as e:
        print(f"Error in update function: {str(e)}")  # Debug log
        db.rollback()
        raise

def remove(db: Session, *, id: int) -> User:
    obj = db.query(User).get(id)
    db.delete(obj)
    db.commit()
    return obj

def authenticate(db: Session, *, username: str, password: str) -> Optional[User]:
    user = get_by_username(db, username=username)
    if not user:
        return None
    
    if not verify_password(password, user.password):
        return None
    
    return user

def is_active(user: User) -> bool:
    return True

def is_admin(user: User) -> bool:
    return user.is_admin if user else False