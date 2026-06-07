from sqlalchemy import Column, Integer, String

from model.base import Base


class Contraindication(Base):
    id   = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
