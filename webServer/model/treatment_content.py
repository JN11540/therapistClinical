from sqlalchemy import Column, Float, Integer, ForeignKey

from model.base import Base


class TreatmentContent(Base):
    id             = Column(Integer, primary_key=True, autoincrement=True)
    treatment_id   = Column(Integer, ForeignKey("treatment.id"), nullable=False)
    exercise_id    = Column(Integer, ForeignKey("exercise.id"), nullable=False)
    sets           = Column(Integer, nullable=False)
    reps           = Column(Integer, nullable=False)
    set_rest_time  = Column(Integer, nullable=False)
    es_intensity   = Column(Float, nullable=True)
    es_frequency   = Column(Float, nullable=True)
    es_pulse_width = Column(Float, nullable=True)
    date           = Column(Integer, nullable=False)
