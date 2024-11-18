from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from ..models import Monkey
from ..schemas.monkey import MonkeyCreate, MonkeyUpdate
from sqlalchemy import extract

def get(db: Session, id: int) -> Optional[Monkey]:
    return db.query(Monkey).filter(Monkey.id == id).first()

def get_by_code(db: Session, code: str) -> Optional[Monkey]:
    return db.query(Monkey).filter(Monkey.code == code).first()

def get_multi(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    filters: Dict[str, Any] = None
) -> List[Monkey]:
    query = db.query(Monkey)
    
    if filters:
        if filters.get("year"):
            query = query.filter(extract('year', Monkey.birthday) == int(filters["year"]))
        if filters.get("date_from"):
            query = query.filter(Monkey.birthday >= datetime.strptime(filters["date_from"], '%Y-%m-%d').date())
        if filters.get("date_to"):
            query = query.filter(Monkey.birthday <= datetime.strptime(filters["date_to"], '%Y-%m-%d').date())
        if filters.get("case_id"):
            query = query.filter(Monkey.case_id == filters["case_id"])
        if filters.get("gender"):
            query = query.filter(Monkey.gender == filters["gender"])
        if filters.get("father"):
            query = query.filter(Monkey.father == filters["father"])
        if filters.get("mother"):
            query = query.filter(Monkey.mother == filters["mother"])
    
    return query.order_by(Monkey.date_created.desc()).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: MonkeyCreate) -> Monkey:
    db_obj = Monkey(
        code=obj_in.code,
        case_id=obj_in.case_id,
        birthday=obj_in.birthday,
        gender=obj_in.gender,
        father=obj_in.father,
        mother=obj_in.mother,
        special_characteristics=obj_in.special_characteristics
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session,
    *,
    db_obj: Monkey,
    obj_in: Union[MonkeyUpdate, Dict[str, Any]]
) -> Monkey:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, id: int) -> Monkey:
    obj = db.query(Monkey).get(id)
    db.delete(obj)
    db.commit()
    return obj

def get_count(db: Session, filters: Dict[str, Any] = None) -> int:
    query = db.query(Monkey)
    
    if filters:
        if filters.get("year"):
            query = query.filter(extract('year', Monkey.birthday) == int(filters["year"]))
        if filters.get("date_from") and filters.get("date_to"):
            query = query.filter(
                and_(
                    Monkey.birthday >= filters["date_from"],
                    Monkey.birthday <= filters["date_to"]
                )
            )
        if filters.get("case_id"):
            query = query.filter(Monkey.case_id == int(filters["case_id"]))
        if filters.get("gender"):
            query = query.filter(Monkey.gender == filters["gender"])
        if filters.get("father"):
            query = query.filter(Monkey.father == filters["father"])
        if filters.get("mother"):
            query = query.filter(Monkey.mother == filters["mother"])
    
    return query.count()