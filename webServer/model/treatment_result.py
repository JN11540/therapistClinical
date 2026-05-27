from sqlalchemy import Column, Integer, ForeignKey

from model.base import Base


class TreatmentResult(Base):
    id                   = Column(Integer, primary_key=True, autoincrement=True)
    treatment_id         = Column(Integer, ForeignKey("treatment.id"), nullable=False)
    treatment_content_id = Column(Integer, ForeignKey("treatment_content.id"), nullable=False)
    reps                 = Column(Integer, nullable=False)
    total_time           = Column(Integer, nullable=False)
    date                 = Column(Integer, nullable=False)
