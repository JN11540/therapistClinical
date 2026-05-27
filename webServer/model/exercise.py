from sqlalchemy import Column, Integer, String

from model.base import Base


class Exercise(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    rep_stage1 = Column(Integer, nullable=False)
    rep_stage2 = Column(Integer, nullable=False)
    rep_stage3 = Column(Integer, nullable=True)
    rep_stage4 = Column(Integer, nullable=True)
