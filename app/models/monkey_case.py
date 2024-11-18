from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class MonkeyCase(Base):
    __tablename__ = "monkey_cases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # This will store the house/case number
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with monkeys
    monkeys = relationship("Monkey", back_populates="case")