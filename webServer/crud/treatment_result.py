from typing import List

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from model.treatment_result import TreatmentResult
from schema.treatment_result import TreatmentResultCreate, TreatmentResultUpdate


class CRUDTreatmentResult(CRUDBase[TreatmentResult, TreatmentResultCreate, TreatmentResultUpdate]):
    def __init__(self):
        super().__init__(TreatmentResult)

    async def get_by_treatment_id(self, session: AsyncSession, treatment_id: int) -> List[TreatmentResult]:
        return await self.get_multi(session, treatment_id=treatment_id)

    async def get_by_content_id(self, session: AsyncSession, treatment_content_id: int) -> List[TreatmentResult]:
        return await self.get_multi(session, treatment_content_id=treatment_content_id)

    async def delete_by_treatment_id(self, session: AsyncSession, treatment_id: int) -> None:
        await session.execute(delete(TreatmentResult).where(TreatmentResult.treatment_id == treatment_id))
        await session.commit()
