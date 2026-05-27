from typing import List

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from model.treatment_content import TreatmentContent
from schema.treatment import TreatmentContentCreate, TreatmentContentUpdate


class CRUDTreatmentContent(CRUDBase[TreatmentContent, TreatmentContentCreate, TreatmentContentUpdate]):
    def __init__(self):
        super().__init__(TreatmentContent)

    async def get_by_treatment_id(self, session: AsyncSession, treatment_id: int) -> List[TreatmentContent]:
        return await self.get_multi(session, treatment_id=treatment_id)

    async def delete_by_treatment_id(self, session: AsyncSession, treatment_id: int) -> None:
        await session.execute(delete(TreatmentContent).where(TreatmentContent.treatment_id == treatment_id))
        await session.commit()
