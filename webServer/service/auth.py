from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.httpResponseMethod import HttpResponseMethod
from core.redis import Redis
from core.security import Security
from crud.clinician import CRUDClinician
from schema.auth import LoginRequest


class AuthService:

    def __init__(self):
        self.crud_clinician = CRUDClinician()

    async def login(self, session: AsyncSession, redis: Redis, data: LoginRequest):
        try:
            clinician = await self.crud_clinician.get(session, username=data.username)
            if clinician is None:
                return await HttpResponseMethod.not_found(
                    message="Clinician not found"
                )
            if not Security.verify_password(data.password, clinician.password_hash):
                return await HttpResponseMethod.bad_request(
                    message="Invalid password"
                )
            session_id = await Security.create_session(redis, clinician.id)
            response = RedirectResponse(url="/home", status_code=307)
            response.set_cookie(key="session_id", value=session_id, httponly=False, samesite="lax")
            response.set_cookie(key="clinician_id", value=str(clinician.id), httponly=False, samesite="lax")
            return response
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def logout(self, request: Request, redis: Redis):
        try:
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return await HttpResponseMethod.bad_request(
                    message="Missing or invalid Authorization header"
                )
            session_id = auth_header.split(" ", 1)[1]
            await Security.delete_session(redis, session_id)
            return await HttpResponseMethod.ok(message="Logged out successfully")
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))
