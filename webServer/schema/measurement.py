from typing import List, Optional
from pydantic import BaseModel

from schema.objective_measurement import ObjectiveMeasurementItem


class CreateRequest(BaseModel):
    patient_id: int
    name: str
    measured_at: int
    sf_36_total: Optional[int] = None
    womac_total: Optional[int] = None
    koos_total: Optional[int] = None


class UpdateRequest(BaseModel):
    id: int
    name: Optional[str] = None
    measured_at: Optional[int] = None
    sf_36_total: Optional[int] = None
    womac_total: Optional[int] = None
    koos_total: Optional[int] = None


class MeasurementCreate(BaseModel):
    patient_id: int
    name: str
    measured_at: int
    sf_36_total: Optional[int] = None
    womac_total: Optional[int] = None
    koos_total: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None


class MeasurementUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    measured_at: Optional[int] = None
    sf_36_total: Optional[int] = None
    womac_total: Optional[int] = None
    koos_total: Optional[int] = None
    updated_at: Optional[int] = None


class MeasurementResponse(BaseModel):
    id: int
    patient_id: int
    name: str
    measured_at: int
    sf_36_total: Optional[int] = None
    womac_total: Optional[int] = None
    koos_total: Optional[int] = None
    created_at: int
    updated_at: int

    model_config = {"from_attributes": True}


class MeasurementFullCreateRequest(BaseModel):
    patient_id: int
    name: str
    measured_at: int
    sf_36_total: Optional[int] = None
    womac_total: Optional[int] = None
    koos_total: Optional[int] = None
    objective: List[ObjectiveMeasurementItem]


class MeasurementFullUpdateRequest(BaseModel):
    id: int
    name: Optional[str] = None
    measured_at: Optional[int] = None
    sf_36_total: Optional[int] = None
    womac_total: Optional[int] = None
    koos_total: Optional[int] = None
    objective: Optional[List[ObjectiveMeasurementItem]] = None


class MeasurementFullResponse(BaseModel):
    id: int
    patient_id: int
    name: str
    measured_at: int
    sf_36_total: Optional[int] = None
    womac_total: Optional[int] = None
    koos_total: Optional[int] = None
    created_at: int
    updated_at: int
    objective: List[ObjectiveMeasurementItem]


class MeasurementListItem(BaseModel):
    id: int
    name: str
    measured_at: int
    sf_36_total: Optional[int] = None
    womac_total: Optional[int] = None
    koos_total: Optional[int] = None
    objective: List[ObjectiveMeasurementItem]
