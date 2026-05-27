from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from schema.exercise import ExerciseCreateRequest, ExerciseUpdateRequest
from service.exercise import ExerciseService

router = APIRouter(prefix="/exercises", tags=["exercises"])

_service = ExerciseService()


@router.post("")
async def create_exercise(
    data: ExerciseCreateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.create(session, data)


@router.get("")
async def get_all_exercises(
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_all(session)


@router.get("/{exercise_id}")
async def get_exercise(
    exercise_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.get_by_id(session, exercise_id)


@router.put("")
async def update_exercise(
    data: ExerciseUpdateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.update(session, data)


@router.delete("/{exercise_id}")
async def delete_exercise(
    exercise_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await _service.delete(session, exercise_id)
