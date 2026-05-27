from sqlalchemy.ext.asyncio import AsyncSession

from core.httpResponseMethod import HttpResponseMethod
from crud.patient import CRUDPatient
from crud.measurement import CRUDMeasurement
from crud.objective_measurement import CRUDObjectiveMeasurement
from schema.measurement import (
    CreateRequest, UpdateRequest, MeasurementCreate, MeasurementUpdate, MeasurementResponse,
    MeasurementFullCreateRequest, MeasurementFullUpdateRequest, MeasurementFullResponse,
)
from schema.objective_measurement import ObjectiveMeasurementCreate, ObjectiveMeasurementItem
from util.datetimeConverter import datetimeConverter


class MeasurementService:

    def __init__(self):
        self.crud_measurement = CRUDMeasurement()
        self.crud_patient = CRUDPatient()
        self.crud_obj = CRUDObjectiveMeasurement()

    async def create(self, session: AsyncSession, data: CreateRequest):
        try:
            patient = await self.crud_patient.get(session, id=data.patient_id)
            if patient is None:
                return await HttpResponseMethod.not_found(
                    message=f"Patient {data.patient_id} not found"
                )
            cur = datetimeConverter.get_current_timestamp()
            create_data = MeasurementCreate(
                **data.dict(),
                created_at=cur,
                updated_at=cur,
            )
            result = await self.crud_measurement.create(session, obj_in=create_data)
            return await HttpResponseMethod.ok(
                data=MeasurementResponse(**result.dict()).dict(),
                message=f"Measurement {result.id} created successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_by_id(self, session: AsyncSession, measurement_id: int):
        try:
            result = await self.crud_measurement.get(session, id=measurement_id)
            if result is None:
                return await HttpResponseMethod.not_found(
                    message=f"Measurement {measurement_id} not found"
                )
            return await HttpResponseMethod.ok(
                data=MeasurementResponse(**result.dict()).dict(),
                message=f"Measurement {measurement_id} retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def update(self, session: AsyncSession, data: UpdateRequest):
        try:
            measurement_id = data.id
            db_obj = await self.crud_measurement.get(session, id=measurement_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Measurement {measurement_id} not found"
                )
            cur = datetimeConverter.get_current_timestamp()
            update_data = MeasurementUpdate(
                **data.dict(),
                updated_at=cur,
            )
            result = await self.crud_measurement.update(session, obj_in=update_data, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                data=MeasurementResponse(**result.dict()).dict(),
                message=f"Measurement {measurement_id} updated successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def create_full(self, session: AsyncSession, data: MeasurementFullCreateRequest):
        try:
            if not (1 <= len(data.objective) <= 2):
                return await HttpResponseMethod.bad_request(
                    message="objective list must contain 1 or 2 items"
                )
            sides = [item.side for item in data.objective]
            if len(sides) != len(set(sides)):
                return await HttpResponseMethod.bad_request(
                    message="objective items must have unique side values"
                )
            patient = await self.crud_patient.get(session, id=data.patient_id)
            if patient is None:
                return await HttpResponseMethod.not_found(
                    message=f"Patient {data.patient_id} not found"
                )
            cur = datetimeConverter.get_current_timestamp()
            create_data = MeasurementCreate(
                patient_id=data.patient_id,
                name=data.name,
                measured_at=data.measured_at,
                sf_36_total=data.sf_36_total,
                womac_total=data.womac_total,
                koos_total=data.koos_total,
                created_at=cur,
                updated_at=cur,
            )
            measurement = await self.crud_measurement.create(session, obj_in=create_data)
            obj_list = []
            for item in data.objective:
                obj_create = ObjectiveMeasurementCreate(measurement_id=measurement.id, **item.dict())
                obj = await self.crud_obj.create(session, obj_in=obj_create)
                obj_list.append(ObjectiveMeasurementItem(**{k: v for k, v in obj.dict().items() if k not in ("id", "measurement_id")}))
            return await HttpResponseMethod.ok(
                data=MeasurementFullResponse(**measurement.dict(), objective=obj_list).dict(),
                message=f"Measurement {measurement.id} created successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_full(self, session: AsyncSession, measurement_id: int):
        try:
            measurement = await self.crud_measurement.get(session, id=measurement_id)
            if measurement is None:
                return await HttpResponseMethod.not_found(
                    message=f"Measurement {measurement_id} not found"
                )
            objs = await self.crud_obj.get_by_measurement_id(session, measurement_id)
            obj_list = [ObjectiveMeasurementItem(**{k: v for k, v in obj.dict().items() if k not in ("id", "measurement_id")}) for obj in objs]
            return await HttpResponseMethod.ok(
                data=MeasurementFullResponse(**measurement.dict(), objective=obj_list).dict(),
                message=f"Measurement {measurement_id} retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def update_full(self, session: AsyncSession, data: MeasurementFullUpdateRequest):
        try:
            measurement_id = data.id
            db_obj = await self.crud_measurement.get(session, id=measurement_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Measurement {measurement_id} not found"
                )
            cur = datetimeConverter.get_current_timestamp()
            update_data = MeasurementUpdate(**data.dict(exclude={"objective"}), updated_at=cur)
            measurement = await self.crud_measurement.update(session, obj_in=update_data, db_obj=db_obj)
            if data.objective is not None:
                await self.crud_obj.delete_by_measurement_id(session, measurement_id)
                obj_list = []
                for item in data.objective:
                    obj_create = ObjectiveMeasurementCreate(measurement_id=measurement_id, **item.dict())
                    obj = await self.crud_obj.create(session, obj_in=obj_create)
                    obj_list.append(ObjectiveMeasurementItem(**{k: v for k, v in obj.dict().items() if k not in ("id", "measurement_id")}))
            else:
                objs = await self.crud_obj.get_by_measurement_id(session, measurement_id)
                obj_list = [ObjectiveMeasurementItem(**{k: v for k, v in obj.dict().items() if k not in ("id", "measurement_id")}) for obj in objs]
            return await HttpResponseMethod.ok(
                data=MeasurementFullResponse(**measurement.dict(), objective=obj_list).dict(),
                message=f"Measurement {measurement_id} updated successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def delete_full(self, session: AsyncSession, measurement_id: int):
        try:
            db_obj = await self.crud_measurement.get(session, id=measurement_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Measurement {measurement_id} not found"
                )
            await self.crud_obj.delete_by_measurement_id(session, measurement_id)
            await self.crud_measurement.delete(session, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                message=f"Measurement {measurement_id} deleted successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def delete(self, session: AsyncSession, measurement_id: int):
        try:
            db_obj = await self.crud_measurement.get(session, id=measurement_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Measurement {measurement_id} not found"
                )
            await self.crud_measurement.delete(session, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                message=f"Measurement {measurement_id} deleted successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))
