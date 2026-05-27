from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from schema.treatment_result import CreateRequest, UpdateRequest
from service.treatment_result import TreatmentResultService

router = APIRouter(prefix="/treatment-results", tags=["treatment-results"])

_service = TreatmentResultService()


@router.post("")
async def create_treatment_result(
    data: CreateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.create(session, data)


@router.get("/by-treatment/{treatment_id}")
async def get_results_by_treatment(
    treatment_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_by_treatment_id(session, treatment_id)


@router.get("/by-content/{treatment_content_id}")
async def get_results_by_content(
    treatment_content_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_by_content_id(session, treatment_content_id)


@router.get("/{result_id}")
async def get_treatment_result(
    result_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_by_id(session, result_id)


@router.put("")
async def update_treatment_result(
    data: UpdateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.update(session, data)


@router.delete("/{result_id}")
async def delete_treatment_result(
    result_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.delete(session, result_id)
