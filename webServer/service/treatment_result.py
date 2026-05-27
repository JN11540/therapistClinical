from sqlalchemy.ext.asyncio import AsyncSession

from core.httpResponseMethod import HttpResponseMethod
from crud.exercise import CRUDExercise
from crud.treatment import CRUDTreatment
from crud.treatment_content import CRUDTreatmentContent
from crud.treatment_result import CRUDTreatmentResult
from schema.treatment_result import (
    CreateRequest, UpdateRequest,
    TreatmentResultCreate, TreatmentResultUpdate, TreatmentResultResponse,
)


class TreatmentResultService:

    def __init__(self):
        self.crud_result    = CRUDTreatmentResult()
        self.crud_treatment = CRUDTreatment()
        self.crud_content   = CRUDTreatmentContent()
        self.crud_exercise  = CRUDExercise()

    @staticmethod
    def _plan_total_time(content, exercise) -> int:
        rep_total = (
            (exercise.rep_stage1 or 0) +
            (exercise.rep_stage2 or 0) +
            (exercise.rep_stage3 or 0) +
            (exercise.rep_stage4 or 0)
        )
        return 10 + content.sets * content.reps * rep_total + content.set_rest_time * (content.sets - 1)

    async def create(self, session: AsyncSession, data: CreateRequest):
        try:
            treatment = await self.crud_treatment.get(session, id=data.treatment_id)
            if treatment is None:
                return await HttpResponseMethod.not_found(
                    message=f"Treatment {data.treatment_id} not found"
                )
            items = []
            for item in data.contents:
                content = await self.crud_content.get(session, id=item.treatment_content_id)
                if content is None:
                    return await HttpResponseMethod.not_found(
                        message=f"TreatmentContent {item.treatment_content_id} not found"
                    )
                exercise = await self.crud_exercise.get(session, id=content.exercise_id)
                ptt = self._plan_total_time(content, exercise)
                create_data = TreatmentResultCreate(
                    treatment_id=data.treatment_id,
                    treatment_content_id=item.treatment_content_id,
                    reps=item.reps,
                    total_time=item.total_time,
                    date=item.date,
                )
                result = await self.crud_result.create(session, obj_in=create_data)
                items.append(TreatmentResultResponse(**result.dict(), plan_total_time=ptt).dict())
            return await HttpResponseMethod.ok(
                data={"treatment_id": data.treatment_id, "contents": items},
                message="TreatmentResult list created successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_by_id(self, session: AsyncSession, result_id: int):
        try:
            result = await self.crud_result.get(session, id=result_id)
            if result is None:
                return await HttpResponseMethod.not_found(
                    message=f"TreatmentResult {result_id} not found"
                )
            content  = await self.crud_content.get(session, id=result.treatment_content_id)
            exercise = await self.crud_exercise.get(session, id=content.exercise_id)
            ptt = self._plan_total_time(content, exercise)
            return await HttpResponseMethod.ok(
                data=TreatmentResultResponse(**result.dict(), plan_total_time=ptt).dict(),
                message=f"TreatmentResult {result_id} retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_by_treatment_id(self, session: AsyncSession, treatment_id: int):
        try:
            treatment = await self.crud_treatment.get(session, id=treatment_id)
            if treatment is None:
                return await HttpResponseMethod.not_found(
                    message=f"Treatment {treatment_id} not found"
                )
            results  = await self.crud_result.get_by_treatment_id(session, treatment_id)
            contents = await self.crud_content.get_by_treatment_id(session, treatment_id)
            content_map = {c.id: c for c in contents}
            exercise_map = {}
            for c in contents:
                if c.exercise_id not in exercise_map:
                    exercise_map[c.exercise_id] = await self.crud_exercise.get(session, id=c.exercise_id)
            data = []
            for r in results:
                content  = content_map.get(r.treatment_content_id)
                exercise = exercise_map.get(content.exercise_id) if content else None
                ptt = self._plan_total_time(content, exercise) if (content and exercise) else 0
                data.append(TreatmentResultResponse(**r.dict(), plan_total_time=ptt).dict())
            return await HttpResponseMethod.ok(
                data={"treatment_id": treatment_id, "contents": data},
                message=f"TreatmentResults for treatment {treatment_id} retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_by_content_id(self, session: AsyncSession, treatment_content_id: int):
        try:
            content = await self.crud_content.get(session, id=treatment_content_id)
            if content is None:
                return await HttpResponseMethod.not_found(
                    message=f"TreatmentContent {treatment_content_id} not found"
                )
            exercise = await self.crud_exercise.get(session, id=content.exercise_id)
            ptt = self._plan_total_time(content, exercise)
            results = await self.crud_result.get_by_content_id(session, treatment_content_id)
            data = [
                TreatmentResultResponse(**r.dict(), plan_total_time=ptt).dict()
                for r in results
            ]
            return await HttpResponseMethod.ok(
                data=data,
                message=f"TreatmentResults for content {treatment_content_id} retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def update(self, session: AsyncSession, data: UpdateRequest):
        try:
            db_obj = await self.crud_result.get(session, id=data.id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"TreatmentResult {data.id} not found"
                )
            content  = await self.crud_content.get(session, id=db_obj.treatment_content_id)
            exercise = await self.crud_exercise.get(session, id=content.exercise_id)
            ptt = self._plan_total_time(content, exercise)
            update_data = TreatmentResultUpdate(**data.dict(exclude={"id"}))
            result = await self.crud_result.update(session, obj_in=update_data, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                data=TreatmentResultResponse(**result.dict(), plan_total_time=ptt).dict(),
                message=f"TreatmentResult {data.id} updated successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def delete(self, session: AsyncSession, result_id: int):
        try:
            db_obj = await self.crud_result.get(session, id=result_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"TreatmentResult {result_id} not found"
                )
            await self.crud_result.delete(session, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                message=f"TreatmentResult {result_id} deleted successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))
