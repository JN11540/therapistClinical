import time
from typing import Optional
from pydantic import BaseModel

class CreateRequest(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    profession: Optional[str] = None
    specialty: Optional[str] = None
    years_of_experience: Optional[int] = None
    institution: Optional[str] = None
    department: Optional[str] = None
    clinic_location: Optional[str] = None
    username: str
    password: str

class UpdateRequest(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    profession: Optional[str] = None
    specialty: Optional[str] = None
    years_of_experience: Optional[int] = None
    institution: Optional[str] = None
    department: Optional[str] = None
    clinic_location: Optional[str] = None

class ClinicianResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    profession: Optional[str] = None
    specialty: Optional[str] = None
    years_of_experience: Optional[int] = None
    institution: Optional[str] = None
    department: Optional[str] = None
    clinic_location: Optional[str] = None

class ClinicianCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    profession: Optional[str] = None
    specialty: Optional[str] = None
    years_of_experience: Optional[int] = None
    institution: Optional[str] = None
    department: Optional[str] = None
    clinic_location: Optional[str] = None
    username: str
    password_hash: str
    created_at: Optional[int] = None
    updated_at: Optional[int] = None

class ClinicianUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    profession: Optional[str] = None
    specialty: Optional[str] = None
    years_of_experience: Optional[int] = None
    institution: Optional[str] = None
    department: Optional[str] = None
    clinic_location: Optional[str] = None
    updated_at: Optional[int] = None