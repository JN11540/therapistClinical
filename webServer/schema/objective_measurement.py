from typing import Optional
from pydantic import BaseModel



class ObjectiveMeasurementItem(BaseModel):
    side: int
    vas_before_test:          Optional[int]   = None
    vas_after_test:           Optional[int]   = None
    tug_time_seconds:         float
    tug_assistive_device:     Optional[bool]  = None
    tug_comment:              Optional[str]   = None
    ftsst_time_seconds:       float
    ftsst_assistive_device:   Optional[bool]  = None
    ftsst_comment:            Optional[str]   = None
    mwt_10_time_seconds:      float
    mwt_10_assistive_device:  Optional[bool]  = None
    mwt_10_comment:           Optional[str]   = None
    sls_time_seconds:         float
    sls_comment:              Optional[str]   = None
    rom_knee_flexion_min:     int
    rom_knee_flexion_max:     int
    rom_knee_flexion_comment: Optional[str]   = None
    rom_knee_extension_min:   Optional[int]   = None
    rom_knee_extension_max:   Optional[int]   = None
    rom_knee_extension_comment: Optional[str] = None
    mmt_knee_flexion:         int
    mmt_knee_extension:       int
    thigh_circumference:      Optional[float] = None


class CreateRequest(BaseModel):
    measurement_id: int
    side: int
    vas_before_test:          Optional[int]   = None
    vas_after_test:           Optional[int]   = None
    tug_time_seconds:         float
    tug_assistive_device:     Optional[bool]  = None
    tug_comment:              Optional[str]   = None
    ftsst_time_seconds:       float
    ftsst_assistive_device:   Optional[bool]  = None
    ftsst_comment:            Optional[str]   = None
    mwt_10_time_seconds:      float
    mwt_10_assistive_device:  Optional[bool]  = None
    mwt_10_comment:           Optional[str]   = None
    sls_time_seconds:         float
    sls_comment:              Optional[str]   = None
    rom_knee_flexion_min:     int
    rom_knee_flexion_max:     int
    rom_knee_flexion_comment: Optional[str]   = None
    rom_knee_extension_min:   Optional[int]   = None
    rom_knee_extension_max:   Optional[int]   = None
    rom_knee_extension_comment: Optional[str] = None
    mmt_knee_flexion:         int
    mmt_knee_extension:       int
    thigh_circumference:      Optional[float] = None


class UpdateRequest(BaseModel):
    id: int
    vas_before_test:          Optional[int]   = None
    vas_after_test:           Optional[int]   = None
    tug_time_seconds:         Optional[float] = None
    tug_assistive_device:     Optional[bool]  = None
    tug_comment:              Optional[str]   = None
    ftsst_time_seconds:       Optional[float] = None
    ftsst_assistive_device:   Optional[bool]  = None
    ftsst_comment:            Optional[str]   = None
    mwt_10_time_seconds:      Optional[float] = None
    mwt_10_assistive_device:  Optional[bool]  = None
    mwt_10_comment:           Optional[str]   = None
    sls_time_seconds:         Optional[float] = None
    sls_comment:              Optional[str]   = None
    rom_knee_flexion_min:     Optional[int]   = None
    rom_knee_flexion_max:     Optional[int]   = None
    rom_knee_flexion_comment: Optional[str]   = None
    rom_knee_extension_min:   Optional[int]   = None
    rom_knee_extension_max:   Optional[int]   = None
    rom_knee_extension_comment: Optional[str] = None
    mmt_knee_flexion:         Optional[int]   = None
    mmt_knee_extension:       Optional[int]   = None
    thigh_circumference:      Optional[float] = None


class ObjectiveMeasurementCreate(BaseModel):
    measurement_id: int
    side: int
    vas_before_test:          Optional[int]   = None
    vas_after_test:           Optional[int]   = None
    tug_time_seconds:         float
    tug_assistive_device:     Optional[bool]  = None
    tug_comment:              Optional[str]   = None
    ftsst_time_seconds:       float
    ftsst_assistive_device:   Optional[bool]  = None
    ftsst_comment:            Optional[str]   = None
    mwt_10_time_seconds:      float
    mwt_10_assistive_device:  Optional[bool]  = None
    mwt_10_comment:           Optional[str]   = None
    sls_time_seconds:         float
    sls_comment:              Optional[str]   = None
    rom_knee_flexion_min:     int
    rom_knee_flexion_max:     int
    rom_knee_flexion_comment: Optional[str]   = None
    rom_knee_extension_min:   Optional[int]   = None
    rom_knee_extension_max:   Optional[int]   = None
    rom_knee_extension_comment: Optional[str] = None
    mmt_knee_flexion:         int
    mmt_knee_extension:       int
    thigh_circumference:      Optional[float] = None


class ObjectiveMeasurementUpdate(BaseModel):
    id: Optional[int] = None
    vas_before_test:          Optional[int]   = None
    vas_after_test:           Optional[int]   = None
    tug_time_seconds:         Optional[float] = None
    tug_assistive_device:     Optional[bool]  = None
    tug_comment:              Optional[str]   = None
    ftsst_time_seconds:       Optional[float] = None
    ftsst_assistive_device:   Optional[bool]  = None
    ftsst_comment:            Optional[str]   = None
    mwt_10_time_seconds:      Optional[float] = None
    mwt_10_assistive_device:  Optional[bool]  = None
    mwt_10_comment:           Optional[str]   = None
    sls_time_seconds:         Optional[float] = None
    sls_comment:              Optional[str]   = None
    rom_knee_flexion_min:     Optional[int]   = None
    rom_knee_flexion_max:     Optional[int]   = None
    rom_knee_flexion_comment: Optional[str]   = None
    rom_knee_extension_min:   Optional[int]   = None
    rom_knee_extension_max:   Optional[int]   = None
    rom_knee_extension_comment: Optional[str] = None
    mmt_knee_flexion:         Optional[int]   = None
    mmt_knee_extension:       Optional[int]   = None
    thigh_circumference:      Optional[float] = None


class ObjectiveMeasurementResponse(BaseModel):
    id: int
    measurement_id: int
    side: int
    vas_before_test:          Optional[int]   = None
    vas_after_test:           Optional[int]   = None
    tug_time_seconds:         float
    tug_assistive_device:     Optional[bool]  = None
    tug_comment:              Optional[str]   = None
    ftsst_time_seconds:       float
    ftsst_assistive_device:   Optional[bool]  = None
    ftsst_comment:            Optional[str]   = None
    mwt_10_time_seconds:      float
    mwt_10_assistive_device:  Optional[bool]  = None
    mwt_10_comment:           Optional[str]   = None
    sls_time_seconds:         float
    sls_comment:              Optional[str]   = None
    rom_knee_flexion_min:     int
    rom_knee_flexion_max:     int
    rom_knee_flexion_comment: Optional[str]   = None
    rom_knee_extension_min:   Optional[int]   = None
    rom_knee_extension_max:   Optional[int]   = None
    rom_knee_extension_comment: Optional[str] = None
    mmt_knee_flexion:         int
    mmt_knee_extension:       int
    thigh_circumference:      Optional[float] = None

    model_config = {"from_attributes": True}
