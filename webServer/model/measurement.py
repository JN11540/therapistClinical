from sqlalchemy import Column, Integer, Float, String, ForeignKey

from model.base import Base


class Measurement(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    name = Column(String, nullable=False)
    measured_at = Column(Integer, nullable=False)
    sf_36_total = Column(Integer, nullable=True)
    womac_total = Column(Integer, nullable=True)
    koos_total = Column(Integer, nullable=True)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=False)
