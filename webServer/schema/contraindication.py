from typing import Optional
from pydantic import BaseModel


class CreateRequest(BaseModel):
    name: str


class UpdateRequest(BaseModel):
    id: int
    name: str


class ContraindicationCreate(BaseModel):
    id:   Optional[int] = None
    name: str


class ContraindicationUpdate(BaseModel):
    name: Optional[str] = None


class ContraindicationResponse(BaseModel):
    id:   int
    name: str
