from sqlalchemy import Column, Integer, String

from model.base import Base


class Clinician(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    profession = Column(String, nullable=True)
    specialty = Column(String, nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    institution = Column(String, nullable=True)
    department = Column(String, nullable=True)
    clinic_location = Column(String, nullable=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=False)