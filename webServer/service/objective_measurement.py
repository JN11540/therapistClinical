from sqlalchemy.ext.asyncio import AsyncSession

from core.httpResponseMethod import HttpResponseMethod
from crud.measurement import CRUDMeasurement
from crud.objective_measurement import CRUDObjectiveMeasurement
from schema.objective_measurement import CreateRequest, UpdateRequest, ObjectiveMeasurementCreate, ObjectiveMeasurementUpdate, ObjectiveMeasurementResponse


class ObjectiveMeasurementService:

    def __init__(self):
        self.crud = CRUDObjectiveMeasurement()
        self.crud_measurement = CRUDMeasurement()

    async def create(self, session: AsyncSession, data: CreateRequest):
        try:
            measurement = await self.crud_measurement.get(session, id=data.measurement_id)
            if measurement is None:
                return await HttpResponseMethod.not_found(
                    message=f"Measurement {data.measurement_id} not found"
                )
            create_data = ObjectiveMeasurementCreate(**data.dict())
            result = await self.crud.create(session, obj_in=create_data)
            return await HttpResponseMethod.ok(
                data=ObjectiveMeasurementResponse(**result.dict()).dict(),
                message=f"ObjectiveMeasurement {result.id} created successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_by_id(self, session: AsyncSession, obj_id: int):
        try:
            result = await self.crud.get(session, id=obj_id)
            if result is None:
                return await HttpResponseMethod.not_found(
                    message=f"ObjectiveMeasurement {obj_id} not found"
                )
            return await HttpResponseMethod.ok(
                data=ObjectiveMeasurementResponse(**result.dict()).dict(),
                message=f"ObjectiveMeasurement {obj_id} retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def update(self, session: AsyncSession, data: UpdateRequest):
        try:
            obj_id = data.id
            db_obj = await self.crud.get(session, id=obj_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"ObjectiveMeasurement {obj_id} not found"
                )
            update_data = ObjectiveMeasurementUpdate(**data.dict())
            result = await self.crud.update(session, obj_in=update_data, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                data=ObjectiveMeasurementResponse(**result.dict()).dict(),
                message=f"ObjectiveMeasurement {obj_id} updated successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def delete(self, session: AsyncSession, obj_id: int):
        try:
            db_obj = await self.crud.get(session, id=obj_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"ObjectiveMeasurement {obj_id} not found"
                )
            await self.crud.delete(session, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                message=f"ObjectiveMeasurement {obj_id} deleted successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))
