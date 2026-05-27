from typing import Optional
from pydantic import BaseModel


class CreateRequest(BaseModel):
    clinician_id: int
    name: str
    email: str
    height: float
    weight: float
    phone: str
    diagnosis: str
    date_of_birth: int
    gender: int
    profession: Optional[str] = None
    kl_grade: Optional[int] = None
    chief_complaint: Optional[str] = None
    aggravating_factors: Optional[str] = None
    medical_history: Optional[str] = None
    imaging_findings: Optional[str] = None
    symptom_duration_months: Optional[int] = None
    visit_flow: Optional[str] = None
    other_knee_treatment_comment: Optional[str] = None


class UpdateRequest(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    phone: Optional[str] = None
    diagnosis: Optional[str] = None
    profession: Optional[str] = None
    kl_grade: Optional[int] = None
    chief_complaint: Optional[str] = None
    aggravating_factors: Optional[str] = None
    medical_history: Optional[str] = None
    imaging_findings: Optional[str] = None
    symptom_duration_months: Optional[int] = None
    visit_flow: Optional[str] = None
    other_knee_treatment_comment: Optional[str] = None


class PatientCreate(BaseModel):
    clinician_id: int
    name: str
    email: str
    height: float
    weight: float
    phone: str
    diagnosis: str
    date_of_birth: int
    gender: int
    profession: Optional[str] = None
    kl_grade: Optional[int] = None
    chief_complaint: Optional[str] = None
    aggravating_factors: Optional[str] = None
    medical_history: Optional[str] = None
    imaging_findings: Optional[str] = None
    symptom_duration_months: Optional[int] = None
    visit_flow: Optional[str] = None
    other_knee_treatment_comment: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None


class PatientUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    phone: Optional[str] = None
    diagnosis: Optional[str] = None
    profession: Optional[str] = None
    kl_grade: Optional[int] = None
    chief_complaint: Optional[str] = None
    aggravating_factors: Optional[str] = None
    medical_history: Optional[str] = None
    imaging_findings: Optional[str] = None
    symptom_duration_months: Optional[int] = None
    visit_flow: Optional[str] = None
    other_knee_treatment_comment: Optional[str] = None
    updated_at: Optional[int] = None


class PatientResponse(BaseModel):
    id: int
    clinician_id: int
    name: str
    email: str
    height: float
    weight: float
    phone: str
    diagnosis: str
    date_of_birth: int
    gender: int
    profession: Optional[str] = None
    kl_grade: Optional[int] = None
    chief_complaint: Optional[str] = None
    aggravating_factors: Optional[str] = None
    medical_history: Optional[str] = None
    imaging_findings: Optional[str] = None
    symptom_duration_months: Optional[int] = None
    visit_flow: Optional[str] = None
    other_knee_treatment_comment: Optional[str] = None


class PatientListItem(BaseModel):
    patient_id: int
    name: str
    height: float
    weight: float
    phone: str
    diagnosis: str
    date_of_birth: int
    gender: int
    profession: Optional[str] = None
    kl_grade: Optional[int] = None
    chief_complaint: Optional[str] = None
    aggravating_factors: Optional[str] = None
    medical_history: Optional[str] = None
    imaging_findings: Optional[str] = None
    symptom_duration_months: Optional[int] = None
    visit_flow: Optional[str] = None
    other_knee_treatment_comment: Optional[str] = None
