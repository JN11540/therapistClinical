from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.httpResponseMethod import HttpResponseMethod
from core.security import Security
from crud.clinician import CRUDClinician
from schema.auth import LoginRequest


class AuthService:

    def __init__(self):
        self.crud_clinician = CRUDClinician()

    async def login(self, session: AsyncSession, data: LoginRequest):
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
            return JSONResponse(content={"status": "ok", "clinician_id": clinician.id})
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def logout(self):
        try:
            return await HttpResponseMethod.ok(message="Logged out successfully")
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))
