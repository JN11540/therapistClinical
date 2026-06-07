from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from schema.contraindication import CreateRequest, UpdateRequest
from service.contraindication import ContraindicationService

router = APIRouter(prefix="/contraindications", tags=["contraindications"])

_service = ContraindicationService()


@router.get("")
async def get_contraindications(
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_all(session)


@router.post("")
async def create_contraindication(
    data: CreateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.create(session, data)


@router.put("")
async def update_contraindication(
    data: UpdateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.update(session, data)


@router.get("/{contraindication_id}")
async def get_contraindication(
    contraindication_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_by_id(session, contraindication_id)


@router.delete("/{contraindication_id}")
async def delete_contraindication(
    contraindication_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.delete(session, contraindication_id)
