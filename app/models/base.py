from datetime import datetime
from sqlalchemy import Column, DateTime
from ..database import Base as DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)