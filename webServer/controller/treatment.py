from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from schema.treatment import CreateRequest, UpdateRequest, TreatmentFullCreateRequest, TreatmentFullUpdateRequest
from service.treatment import TreatmentService

router = APIRouter(prefix="/treatments", tags=["treatments"])

_service = TreatmentService()


@router.post("")
async def create_treatment(
    data: CreateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.create(session, data)


@router.post("/full")
async def create_treatment_full(
    data: TreatmentFullCreateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.create_full(session, data)


@router.get("/patient/{patient_id}")
async def get_treatments_by_patient(
    patient_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_by_patient_id(session, patient_id)


@router.get("/{treatment_id}/full")
async def get_treatment_full(
    treatment_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_full(session, treatment_id)


@router.get("/{treatment_id}/qrcode")
async def get_treatment_qrcode(
    treatment_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_qrcode(session, treatment_id)


@router.post("/{treatment_id}/send-email")
async def send_treatment_email(
    treatment_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.send_email(session, treatment_id)


@router.get("/{treatment_id}")
async def get_treatment(
    treatment_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_by_id(session, treatment_id)


@router.put("/full")
async def update_treatment_full(
    data: TreatmentFullUpdateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.update_full(session, data)


@router.put("")
async def update_treatment(
    data: UpdateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.update(session, data)


@router.delete("/{treatment_id}/full")
async def delete_treatment_full(
    treatment_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.delete_full(session, treatment_id)


@router.delete("/{treatment_id}")
async def delete_treatment(
    treatment_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.delete(session, treatment_id)
