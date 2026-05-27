from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from schema.measurement import CreateRequest, UpdateRequest, MeasurementFullCreateRequest, MeasurementFullUpdateRequest
from service.measurement import MeasurementService

router = APIRouter(prefix="/measurements", tags=["measurements"])

_service = MeasurementService()


@router.post("")
async def create_measurement(
    data: CreateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.create(session, data)


@router.post("/full")
async def create_measurement_full(
    data: MeasurementFullCreateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.create_full(session, data)


@router.get("/{measurement_id}/full")
async def get_measurement_full(
    measurement_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_full(session, measurement_id)


@router.put("/full")
async def update_measurement_full(
    data: MeasurementFullUpdateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.update_full(session, data)


@router.get("/{measurement_id}")
async def get_measurement(
    measurement_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_by_id(session, measurement_id)


@router.put("")
async def update_measurement(
    data: UpdateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.update(session, data)


@router.delete("/{measurement_id}/full")
async def delete_measurement_full(
    measurement_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.delete_full(session, measurement_id)


@router.delete("/{measurement_id}")
async def delete_measurement(
    measurement_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.delete(session, measurement_id)
