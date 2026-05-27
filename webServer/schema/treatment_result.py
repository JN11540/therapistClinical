from typing import List, Optional

from pydantic import BaseModel


class ContentCreateItem(BaseModel):
    treatment_content_id: int
    reps: int
    total_time: int
    date: int


class CreateRequest(BaseModel):
    treatment_id: int
    contents: List[ContentCreateItem]


class UpdateRequest(BaseModel):
    id: int
    reps: Optional[int] = None
    total_time: Optional[int] = None
    date: Optional[int] = None


class TreatmentResultCreate(BaseModel):
    treatment_id: int
    treatment_content_id: int
    reps: int
    total_time: int
    date: int


class TreatmentResultUpdate(BaseModel):
    reps: Optional[int] = None
    total_time: Optional[int] = None
    date: Optional[int] = None


class TreatmentResultResponse(BaseModel):
    id: int
    treatment_content_id: int
    reps: int
    total_time: int
    date: int
    plan_total_time: int

    model_config = {"from_attributes": True}
