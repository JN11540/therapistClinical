from typing import List

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from model.objective_measurement import ObjectiveMeasurement
from schema.objective_measurement import ObjectiveMeasurementCreate, ObjectiveMeasurementUpdate


class CRUDObjectiveMeasurement(CRUDBase[ObjectiveMeasurement, ObjectiveMeasurementCreate, ObjectiveMeasurementUpdate]):
    def __init__(self):
        super().__init__(ObjectiveMeasurement)

    async def get_by_measurement_id(self, session: AsyncSession, measurement_id: int) -> List[ObjectiveMeasurement]:
        return await self.get_multi(session, measurement_id=measurement_id)

    async def delete_by_measurement_id(self, session: AsyncSession, measurement_id: int) -> None:
        await session.execute(delete(ObjectiveMeasurement).where(ObjectiveMeasurement.measurement_id == measurement_id))
        await session.commit()
