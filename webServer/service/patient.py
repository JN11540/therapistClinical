from sqlalchemy.ext.asyncio import AsyncSession

from core.httpResponseMethod import HttpResponseMethod
from crud.clinician import CRUDClinician
from crud.patient import CRUDPatient
from crud.measurement import CRUDMeasurement
from crud.objective_measurement import CRUDObjectiveMeasurement
from crud.treatment import CRUDTreatment
from crud.treatment_content import CRUDTreatmentContent
from crud.treatment_result import CRUDTreatmentResult
from schema.patient import CreateRequest, UpdateRequest, PatientCreate, PatientUpdate, PatientResponse
from schema.measurement import MeasurementListItem
from schema.objective_measurement import ObjectiveMeasurementItem
from util.datetimeConverter import datetimeConverter


class PatientService:

    def __init__(self):
        self.crud_patient = CRUDPatient()
        self.crud_clinician = CRUDClinician()
        self.crud_measurement = CRUDMeasurement()
        self.crud_obj = CRUDObjectiveMeasurement()
        self.crud_treatment = CRUDTreatment()
        self.crud_content = CRUDTreatmentContent()
        self.crud_result = CRUDTreatmentResult()

    async def create(self, session: AsyncSession, data: CreateRequest):
        try:
            clinician = await self.crud_clinician.get(session, id=data.clinician_id)
            if clinician is None:
                return await HttpResponseMethod.not_found(
                    message=f"Clinician {data.clinician_id} not found"
                )
            cur = datetimeConverter.get_current_timestamp()
            create_data = PatientCreate(
                **data.dict(),
                created_at=cur,
                updated_at=cur,
            )
            result = await self.crud_patient.create(session, obj_in=create_data)
            return await HttpResponseMethod.ok(
                data=PatientResponse(**result.dict()).dict(),
                message=f"Patient {result.id} created successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_by_id(self, session: AsyncSession, patient_id: int):
        try:
            result = await self.crud_patient.get(session, id=patient_id)
            if result is None:
                return await HttpResponseMethod.not_found(
                    message=f"Patient {patient_id} not found"
                )
            return await HttpResponseMethod.ok(
                data=PatientResponse(**result.dict()).dict(),
                message=f"Patient {patient_id} retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def update(self, session: AsyncSession, data: UpdateRequest):
        try:
            patient_id = data.id
            db_obj = await self.crud_patient.get(session, id=patient_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Patient {patient_id} not found"
                )
            cur = datetimeConverter.get_current_timestamp()
            update_data = PatientUpdate(
                **data.dict(),
                updated_at=cur,
            )
            result = await self.crud_patient.update(session, obj_in=update_data, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                data=PatientResponse(**result.dict()).dict(),
                message=f"Patient {patient_id} updated successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_measurements(self, session: AsyncSession, patient_id: int):
        try:
            patient = await self.crud_patient.get(session, id=patient_id)
            if patient is None:
                return await HttpResponseMethod.not_found(
                    message=f"Patient {patient_id} not found"
                )
            measurements = await self.crud_measurement.get_multi(session, patient_id=patient_id)
            result = []
            for m in measurements:
                objs = await self.crud_obj.get_by_measurement_id(session, m.id)
                obj_list = [
                    ObjectiveMeasurementItem(**{k: v for k, v in obj.dict().items() if k not in ("id", "measurement_id")})
                    for obj in objs
                ]
                result.append(MeasurementListItem(
                    id=m.id,
                    name=m.name,
                    measured_at=m.measured_at,
                    sf_36_total=m.sf_36_total,
                    womac_total=m.womac_total,
                    koos_total=m.koos_total,
                    objective=obj_list,
                ).dict())
            return await HttpResponseMethod.ok(
                data=result,
                message=f"Measurements for patient {patient_id} retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def delete(self, session: AsyncSession, patient_id: int):
        try:
            db_obj = await self.crud_patient.get(session, id=patient_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Patient {patient_id} not found"
                )
            treatments = await self.crud_treatment.get_multi(session, patient_id=patient_id)
            for t in treatments:
                await self.crud_result.delete_by_treatment_id(session, t.id)
                await self.crud_content.delete_by_treatment_id(session, t.id)
                await self.crud_treatment.delete(session, db_obj=t)
            measurements = await self.crud_measurement.get_multi(session, patient_id=patient_id)
            for m in measurements:
                await self.crud_obj.delete_by_measurement_id(session, m.id)
                await self.crud_measurement.delete(session, db_obj=m)
            await self.crud_patient.delete(session, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                message=f"Patient {patient_id} deleted successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))
