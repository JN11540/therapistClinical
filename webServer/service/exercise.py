import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import Settings, EXERCISE_JSON
from core.database import engine
from core.httpResponseMethod import HttpResponseMethod
from crud.exercise import CRUDExercise
from schema.exercise import ExerciseCreateRequest, ExerciseUpdateRequest, ExerciseCreate, ExerciseUpdate, ExerciseResponse


class ExerciseService:

    def __init__(self):
        self.crud_exercise = CRUDExercise()

    async def seed_exercises(self) -> None:
        async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with async_session() as session:
            existing = await self.crud_exercise.get_multi(session, limit=1)
            if existing:
                return

            with open(EXERCISE_JSON, encoding="utf-8") as f:
                exercises = json.load(f)

            exercises.sort(key=lambda x: x["id"])

            for item in exercises:
                await self.crud_exercise.create(session, obj_in=ExerciseCreate(
                    id=item["id"],
                    name=item["name"],
                    rep_stage1=item["rep_stage1"],
                    rep_stage2=item["rep_stage2"],
                    rep_stage3=item["rep_stage3"],
                    rep_stage4=item["rep_stage4"],
                ))

    async def create(self, session: AsyncSession, data: ExerciseCreateRequest):
        try:
            create_data = ExerciseCreate(
                name=data.name,
                rep_stage1=data.rep_stage1,
                rep_stage2=data.rep_stage2,
                rep_stage3=data.rep_stage3,
                rep_stage4=data.rep_stage4,
            )
            result = await self.crud_exercise.create(session, obj_in=create_data)
            return await HttpResponseMethod.ok(
                data=ExerciseResponse(**result.dict()).dict(),
                message=f"Exercise {result.id} created successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_all(self, session: AsyncSession):
        try:
            results = await self.crud_exercise.get_multi(session)
            return await HttpResponseMethod.ok(
                data=[ExerciseResponse(**r.dict()).dict() for r in results],
                message="Exercises retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_by_id(self, session: AsyncSession, exercise_id: int):
        try:
            result = await self.crud_exercise.get(session, id=exercise_id)
            if result is None:
                return await HttpResponseMethod.not_found(
                    message=f"Exercise {exercise_id} not found"
                )
            return await HttpResponseMethod.ok(
                data=ExerciseResponse(**result.dict()).dict(),
                message=f"Exercise {exercise_id} retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def update(self, session: AsyncSession, data: ExerciseUpdateRequest):
        try:
            db_obj = await self.crud_exercise.get(session, id=data.id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Exercise {data.id} not found"
                )
            update_data = ExerciseUpdate(
                name=data.name,
                rep_stage1=data.rep_stage1,
                rep_stage2=data.rep_stage2,
                rep_stage3=data.rep_stage3,
                rep_stage4=data.rep_stage4,
            )
            result = await self.crud_exercise.update(session, obj_in=update_data, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                data=ExerciseResponse(**result.dict()).dict(),
                message=f"Exercise {data.id} updated successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def delete(self, session: AsyncSession, exercise_id: int):
        try:
            db_obj = await self.crud_exercise.get(session, id=exercise_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Exercise {exercise_id} not found"
                )
            await self.crud_exercise.delete(session, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                message=f"Exercise {exercise_id} deleted successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))
