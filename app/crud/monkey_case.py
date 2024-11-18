from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import MonkeyCase
from ..schemas.monkey_case import MonkeyCaseCreate, MonkeyCaseUpdate

def get(db: Session, id: int) -> Optional[MonkeyCase]:
    return db.query(MonkeyCase).filter(MonkeyCase.id == id).first()

def get_by_name(db: Session, name: str) -> Optional[MonkeyCase]:
    return db.query(MonkeyCase).filter(MonkeyCase.name == name).first()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[MonkeyCase]:
    return db.query(MonkeyCase).order_by(MonkeyCase.name.asc()).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: MonkeyCaseCreate) -> MonkeyCase:
    db_obj = MonkeyCase(name=obj_in.name)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, *, db_obj: MonkeyCase, obj_in: MonkeyCaseUpdate) -> MonkeyCase:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    for field in ['name']:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, id: int) -> MonkeyCase:
    obj = db.query(MonkeyCase).get(id)
    db.delete(obj)
    db.commit()
    return obj