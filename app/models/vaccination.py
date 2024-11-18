from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True, index=True)
    monkey_id = Column(Integer, ForeignKey("monkeys.id"))
    vaccine_id = Column(Integer, ForeignKey("vaccines.id"))
    date = Column(Date)
    dose = Column(Integer)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    monkey = relationship("Monkey", back_populates="vaccinations")
    vaccine = relationship("Vaccine", back_populates="vaccinations")