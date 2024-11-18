from sqlalchemy import Column, Integer, String, Date, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import enum


class Gender(str, enum.Enum):
    MALE = "M"
    FEMALE = "F"


class Monkey(Base):
    __tablename__ = "monkeys"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    case_id = Column(Integer, ForeignKey("monkey_cases.id"), index=True)  # Foreign key to monkey_cases
    birthday = Column(Date)
    gender = Column(SQLEnum(Gender))
    father = Column(String, nullable=True)
    mother = Column(String, nullable=True)
    special_characteristics = Column(String, nullable=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    case = relationship("MonkeyCase", back_populates="monkeys")
    vaccinations = relationship("Vaccination", back_populates="monkey")