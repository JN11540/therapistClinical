from sqlalchemy import Column, Integer, ForeignKey

from model.base import Base


class TreatmentContent(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    treatment_id = Column(Integer, ForeignKey("treatment.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercise.id"), nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    set_rest_time = Column(Integer, nullable=False)
    date = Column(Integer, nullable=False)
