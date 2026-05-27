from typing import Optional

from pydantic import BaseModel


class ExerciseCreateRequest(BaseModel):
    name: str
    rep_stage1: int
    rep_stage2: int
    rep_stage3: Optional[int] = None
    rep_stage4: Optional[int] = None


class ExerciseUpdateRequest(BaseModel):
    id: int
    name: str
    rep_stage1: int
    rep_stage2: int
    rep_stage3: Optional[int] = None
    rep_stage4: Optional[int] = None


class ExerciseCreate(BaseModel):
    name: str
    rep_stage1: int
    rep_stage2: int
    rep_stage3: Optional[int] = None
    rep_stage4: Optional[int] = None


class ExerciseUpdate(BaseModel):
    name: str
    rep_stage1: int
    rep_stage2: int
    rep_stage3: Optional[int] = None
    rep_stage4: Optional[int] = None


class ExerciseResponse(BaseModel):
    id: int
    name: str
    rep_stage1: int
    rep_stage2: int
    rep_stage3: Optional[int] = None
    rep_stage4: Optional[int] = None

    model_config = {"from_attributes": True}
