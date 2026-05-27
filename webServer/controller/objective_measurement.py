from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from schema.objective_measurement import CreateRequest, UpdateRequest
from service.objective_measurement import ObjectiveMeasurementService

router = APIRouter(prefix="/objective-measurements", tags=["objective-measurements"])

_service = ObjectiveMeasurementService()


@router.post("")
async def create_objective_measurement(
    data: CreateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.create(session, data)


@router.get("/{obj_id}")
async def get_objective_measurement(
    obj_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_by_id(session, obj_id)


@router.put("")
async def update_objective_measurement(
    data: UpdateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.update(session, data)


@router.delete("/{obj_id}")
async def delete_objective_measurement(
    obj_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.delete(session, obj_id)
