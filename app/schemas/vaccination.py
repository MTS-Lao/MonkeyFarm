# app/schemas/vaccination.py
from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime

class VaccinationBase(BaseModel):
    monkey_id: int
    vaccine_id: int
    date: date
    dose: int

class VaccinationCreate(VaccinationBase):
    pass

class VaccinationUpdate(VaccinationBase):
    pass

class Vaccination(VaccinationBase):
    id: int
    date_created: datetime
    date_updated: Optional[datetime] = None

    class Config:
        from_attributes = True

class VaccinationWithDetails(Vaccination):
    monkey: "MonkeyBase"
    vaccine: "VaccineBase"

    class Config:
        from_attributes = True

# Import at the end to avoid circular imports
from .monkey import MonkeyBase  # noqa
from .vaccine import VaccineBase  # noqa
VaccinationWithDetails.model_rebuild()