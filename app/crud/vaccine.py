from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import Vaccine
from ..schemas.vaccine import VaccineCreate, VaccineUpdate

def get(db: Session, id: int) -> Optional[Vaccine]:
    return db.query(Vaccine).filter(Vaccine.id == id).first()

def get_by_name(db: Session, name: str) -> Optional[Vaccine]:
    return db.query(Vaccine).filter(Vaccine.name == name).first()

def get_multi(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
) -> List[Vaccine]:
    return db.query(Vaccine).order_by(Vaccine.name.asc()).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: VaccineCreate) -> Vaccine:
    db_obj = Vaccine(
        name=obj_in.name,
        description=obj_in.description
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session,
    *,
    db_obj: Vaccine,
    obj_in: VaccineUpdate
) -> Vaccine:
    update_data = obj_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, id: int) -> Vaccine:
    obj = db.query(Vaccine).get(id)
    db.delete(obj)
    db.commit()
    return obj