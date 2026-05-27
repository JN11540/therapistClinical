from sqlalchemy import Column, Integer, String, ForeignKey

from model.base import Base


class Treatment(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=True)
