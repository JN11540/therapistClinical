from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

from model.base import Base


class Patient(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    clinician_id = Column(Integer, ForeignKey("clinician.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    phone = Column(String, nullable=False)
    diagnosis = Column(String, nullable=False)
    date_of_birth = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    profession = Column(String, nullable=True)
    kl_grade = Column(Integer, nullable=True)
    chief_complaint = Column(String, nullable=True)
    aggravating_factors = Column(String, nullable=True)
    medical_history = Column(String, nullable=True)
    imaging_findings = Column(String, nullable=True)
    symptom_duration_months = Column(Integer, nullable=True)
    visit_flow = Column(String, nullable=True)
    other_knee_treatment_comment = Column(String, nullable=True)
    contraindications = Column(ARRAY(Integer), nullable=True)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=False)
