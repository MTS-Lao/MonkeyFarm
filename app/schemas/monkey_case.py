from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MonkeyCaseBase(BaseModel):
    name: str


class MonkeyCaseCreate(MonkeyCaseBase):
    pass


class MonkeyCaseUpdate(MonkeyCaseBase):
    pass


class MonkeyCaseInDBBase(MonkeyCaseBase):
    id: int
    date_created: datetime
    date_updated: Optional[datetime] = None

    class Config:
        from_attributes = True


class MonkeyCase(MonkeyCaseInDBBase):
    pass