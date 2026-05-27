from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from core.redis import Redis, get_redis
from schema.auth import LoginRequest
from service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

_service = AuthService()


@router.post("/login")
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
):
    return await _service.login(session, redis, data)


@router.post("/logout")
async def logout(
    request: Request,
    redis: Redis = Depends(get_redis),
):
    return await _service.logout(request, redis)
