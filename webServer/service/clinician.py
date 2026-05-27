from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from core.httpResponseMethod import HttpResponseMethod
from crud.clinician import CRUDClinician
from crud.patient import CRUDPatient
from schema.clinician import CreateRequest, UpdateRequest, ClinicianCreate, ClinicianUpdate, ClinicianResponse
from schema.patient import PatientListItem

from util.datetimeConverter import datetimeConverter

from core.security import Security

class ClinicianService:

    def __init__(self):
        self.crud_clinician = CRUDClinician()
        self.crud_patient = CRUDPatient()

    async def create(self, session: AsyncSession, data: CreateRequest):
        try:
            existing = await self.crud_clinician.get(session, username=data.username)
            if existing is not None:
                return await HttpResponseMethod.bad_request(
                    message=f"Username '{data.username}' already exists"
                )

            cur = datetimeConverter.get_current_timestamp()
            password_hash = Security.hash_password(data.password)

            create_data = ClinicianCreate(
                **data.dict(exclude={"password"}),
                password_hash=password_hash,
                created_at=cur,
                updated_at=cur,
            )

            result = await self.crud_clinician.create(session, obj_in=create_data)
            response_data = ClinicianResponse(**result.dict())

            return await HttpResponseMethod.ok(
                data=response_data.dict(),
                message=f"Clinician {result.id} created successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_by_id(self, session: AsyncSession, clinician_id: int):
        try:
            result = await self.crud_clinician.get(session, id=clinician_id)
            if result is None:
                return await HttpResponseMethod.not_found(
                    message=f"Clinician {clinician_id} not found"
                )
            response_data = ClinicianResponse(**result.dict())
            return await HttpResponseMethod.ok(
                data=response_data.dict(),
                message=f"Clinician {clinician_id} retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def update(self, session: AsyncSession, data: UpdateRequest):
        try:
            clinician_id = data.id
            cur = datetimeConverter.get_current_timestamp()

            db_obj = await self.crud_clinician.get(session, id=clinician_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Clinician {clinician_id} not found"
                )
            update_data = ClinicianUpdate(
                **data.dict(),
                updated_at=cur,
            )
            result = await self.crud_clinician.update(session, obj_in=data, db_obj=db_obj)
            response_data = ClinicianResponse(**result.dict())
            return await HttpResponseMethod.ok(
                data=response_data.dict(),
                message=f"Clinician {clinician_id} updated successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_patients(self, session: AsyncSession, clinician_id: int):
        try:
            clinician = await self.crud_clinician.get(session, id=clinician_id)
            if clinician is None:
                return await HttpResponseMethod.not_found(
                    message=f"Clinician {clinician_id} not found"
                )
            patients = await self.crud_patient.get_multi(session, clinician_id=clinician_id)
            data = [
                PatientListItem(patient_id=p.id, **{
                    k: v for k, v in p.dict().items() if k in PatientListItem.model_fields and k != "patient_id"
                }).dict()
                for p in patients
            ]
            return await HttpResponseMethod.ok(
                data=data,
                message=f"Found {len(data)} patient(s) for clinician {clinician_id}",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def delete(self, session: AsyncSession, clinician_id: int):
        try:
            db_obj = await self.crud_clinician.get(session, id=clinician_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Clinician {clinician_id} not found"
                )
            await self.crud_clinician.delete(session, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                message=f"Clinician {clinician_id} deleted successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))
