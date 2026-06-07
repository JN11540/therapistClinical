from typing import List, Optional

from pydantic import BaseModel


class TreatmentContentInput(BaseModel):
    exercise_id: int
    sets: int
    reps: int
    set_rest_time: int
    es_intensity: Optional[float] = None
    es_frequency: Optional[float] = None
    es_pulse_width: Optional[float] = None
    date: int


class TreatmentContentItem(BaseModel):
    id: int
    exercise_id: int
    sets: int
    reps: int
    set_rest_time: int
    es_intensity: Optional[float] = None
    es_frequency: Optional[float] = None
    es_pulse_width: Optional[float] = None
    date: int


class TreatmentContentCreate(BaseModel):
    treatment_id: int
    exercise_id: int
    sets: int
    reps: int
    set_rest_time: int
    es_intensity: Optional[float] = None
    es_frequency: Optional[float] = None
    es_pulse_width: Optional[float] = None
    date: int


class TreatmentContentUpdate(BaseModel):
    exercise_id: Optional[int] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    set_rest_time: Optional[int] = None
    es_intensity: Optional[float] = None
    es_frequency: Optional[float] = None
    es_pulse_width: Optional[float] = None
    date: Optional[int] = None


class CreateRequest(BaseModel):
    name: str
    patient_id: int
    start_time: int
    end_time: int


class UpdateRequest(BaseModel):
    id: int
    name: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None


class TreatmentCreate(BaseModel):
    name: str
    patient_id: int
    start_time: int
    end_time: int
    created_at: int
    updated_at: Optional[int] = None


class TreatmentUpdate(BaseModel):
    name: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    updated_at: Optional[int] = None


class TreatmentResponse(BaseModel):
    id: int
    name: str
    patient_id: int
    start_time: int
    end_time: int
    created_at: int
    updated_at: Optional[int] = None

    model_config = {"from_attributes": True}


class TreatmentFullCreateRequest(BaseModel):
    name: str
    patient_id: int
    start_time: int
    end_time: int
    contents: List[TreatmentContentInput]


class TreatmentFullUpdateRequest(BaseModel):
    id: int
    name: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    contents: Optional[List[TreatmentContentInput]] = None


class TreatmentFullResponse(BaseModel):
    id: int
    name: str
    patient_id: int
    start_time: int
    end_time: int
    created_at: int
    updated_at: Optional[int] = None
    contents: List[TreatmentContentItem]


class TreatmentListItem(BaseModel):
    id: int
    name: str
    start_time: int
    end_time: int
    contents: List[TreatmentContentItem]
