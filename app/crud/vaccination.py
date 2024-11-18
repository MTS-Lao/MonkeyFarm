from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models import Vaccination
from ..schemas.vaccination import VaccinationCreate, VaccinationUpdate

def get(db: Session, id: int) -> Optional[Vaccination]:
    return db.query(Vaccination).filter(Vaccination.id == id).first()

# Update in app/crud/vaccination.py
def get_multi(
    db: Session,
    skip: int = 0,
    limit: Optional[int] = 100,
    filters: Dict[str, Any] = None
) -> List[Vaccination]:
    query = db.query(Vaccination)
    
    if filters:
        if filters.get("monkey_id"):
            query = query.filter(Vaccination.monkey_id == filters["monkey_id"])
        if filters.get("vaccine_id"):
            query = query.filter(Vaccination.vaccine_id == filters["vaccine_id"])
        if filters.get("dose"):
            query = query.filter(Vaccination.dose == filters["dose"])
        if filters.get("date_from"):
            query = query.filter(Vaccination.date >= datetime.strptime(filters["date_from"], '%Y-%m-%d').date())
        if filters.get("date_to"):
            query = query.filter(Vaccination.date <= datetime.strptime(filters["date_to"], '%Y-%m-%d').date())
    
    query = query.order_by(Vaccination.date.desc())
    
    if limit:
        query = query.offset(skip).limit(limit)
    
    return query.all()

def create(db: Session, *, obj_in: VaccinationCreate) -> Vaccination:
    db_obj = Vaccination(
        monkey_id=obj_in.monkey_id,
        vaccine_id=obj_in.vaccine_id,
        date=obj_in.date,
        dose=obj_in.dose
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session,
    *,
    db_obj: Vaccination,
    obj_in: VaccinationUpdate
) -> Vaccination:
    update_data = obj_in.dict(exclude_unset=True)
    
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, id: int) -> Vaccination:
    obj = db.query(Vaccination).get(id)
    db.delete(obj)
    db.commit()
    return obj

def get_count(db: Session, filters: Dict[str, Any] = None) -> int:
    query = db.query(Vaccination)
    
    if filters:
        if filters.get("monkey_id"):
            query = query.filter(Vaccination.monkey_id == filters["monkey_id"])
        if filters.get("vaccine_id"):
            query = query.filter(Vaccination.vaccine_id == filters["vaccine_id"])
        if filters.get("date_from"):
            query = query.filter(Vaccination.date >= datetime.strptime(filters["date_from"], '%Y-%m-%d').date())
        if filters.get("date_to"):
            query = query.filter(Vaccination.date <= datetime.strptime(filters["date_to"], '%Y-%m-%d').date())
    
    return query.count()