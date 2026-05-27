from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from schema.patient import CreateRequest, UpdateRequest
from service.patient import PatientService

router = APIRouter(prefix="/patients", tags=["patients"])

_service = PatientService()


@router.post("")
async def create_patient(
    data: CreateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.create(session, data)


@router.get("/{patient_id}/measurements")
async def get_patient_measurements(
    patient_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_measurements(session, patient_id)


@router.get("/{patient_id}")
async def get_patient(
    patient_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_by_id(session, patient_id)


@router.put("")
async def update_patient(
    data: UpdateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.update(session, data)


@router.delete("/{patient_id}")
async def delete_patient(
    patient_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.delete(session, patient_id)
