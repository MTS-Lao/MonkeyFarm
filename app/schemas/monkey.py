from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime
from ..models.monkey import Gender

class MonkeyBase(BaseModel):
    code: str
    case_id: int
    birthday: date
    gender: Gender
    father: Optional[str] = None
    mother: Optional[str] = None
    special_characteristics: Optional[str] = None

class MonkeyCreate(MonkeyBase):
    pass

class MonkeyUpdate(MonkeyBase):
    pass

class MonkeyInDBBase(MonkeyBase):
    id: int
    date_created: datetime
    date_updated: Optional[datetime] = None

    class Config:
        from_attributes = True

class Monkey(MonkeyInDBBase):
    pass

class MonkeyWithCase(Monkey):
    case: "MonkeyCaseBase"

from .monkey_case import MonkeyCaseBase  # noqa
MonkeyWithCase.model_rebuild()