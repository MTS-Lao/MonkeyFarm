# app/schemas/vaccine.py

from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class VaccineBase(BaseModel):
    name: str
    description: Optional[str] = None

class VaccineCreate(VaccineBase):
    pass

class VaccineUpdate(VaccineBase):
    pass

class Vaccine(VaccineBase):
    id: int
    date_created: datetime
    date_updated: Optional[datetime] = None

    class Config:
        from_attributes = True

# This is required for SQLAlchemy models
VaccineBase.model_config["from_attributes"] = True