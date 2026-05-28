from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from schema.auth import LoginRequest
from service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

_service = AuthService()


@router.post("/login")
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    return await _service.login(session, data)


@router.post("/logout")
async def logout():
    return await _service.logout()
