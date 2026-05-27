from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from schema.clinician import CreateRequest, UpdateRequest
from service.clinician import ClinicianService

router = APIRouter(prefix="/clinicians", tags=["clinicians"])

_service = ClinicianService()


@router.post("")
async def create_clinician(
    data: CreateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.create(session, data)


@router.get("/{clinician_id}")
async def get_clinician(
    clinician_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_by_id(session, clinician_id)


@router.put("")
async def update_clinician(
    data: UpdateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.update(session, data)


@router.delete("/{clinician_id}")
async def delete_clinician(
    clinician_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.delete(session, clinician_id)


@router.get("/{clinician_id}/patients")
async def get_clinician_patients(
    clinician_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_patients(session, clinician_id)
