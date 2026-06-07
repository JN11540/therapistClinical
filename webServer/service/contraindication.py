import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import CONTRAINDICATION_JSON
from core.database import engine
from core.httpResponseMethod import HttpResponseMethod
from crud.contraindication import CRUDContraindication
from schema.contraindication import CreateRequest, UpdateRequest, ContraindicationCreate, ContraindicationUpdate, ContraindicationResponse


class ContraindicationService:

    def __init__(self):
        self.crud = CRUDContraindication()

    async def seed_contraindications(self) -> None:
        async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with async_session() as session:
            existing = await self.crud.get_multi(session, limit=1)
            if existing:
                return

            with open(CONTRAINDICATION_JSON, encoding="utf-8") as f:
                items = json.load(f)

            items.sort(key=lambda x: x["id"])

            for item in items:
                await self.crud.create(session, obj_in=ContraindicationCreate(
                    id=item["id"],
                    name=item["name"],
                ))

    async def get_all(self, session: AsyncSession):
        try:
            results = await self.crud.get_multi(session)
            return await HttpResponseMethod.ok(
                data=[ContraindicationResponse(**r.dict()).dict() for r in results],
                message="Contraindications retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_by_id(self, session: AsyncSession, contraindication_id: int):
        try:
            result = await self.crud.get(session, id=contraindication_id)
            if result is None:
                return await HttpResponseMethod.not_found(
                    message=f"Contraindication {contraindication_id} not found"
                )
            return await HttpResponseMethod.ok(
                data=ContraindicationResponse(**result.dict()).dict(),
                message=f"Contraindication {contraindication_id} retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def create(self, session: AsyncSession, data: CreateRequest):
        try:
            result = await self.crud.create(session, obj_in=ContraindicationCreate(name=data.name))
            return await HttpResponseMethod.ok(
                data=ContraindicationResponse(**result.dict()).dict(),
                message=f"Contraindication {result.id} created successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def update(self, session: AsyncSession, data: UpdateRequest):
        try:
            db_obj = await self.crud.get(session, id=data.id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Contraindication {data.id} not found"
                )
            result = await self.crud.update(session, obj_in=ContraindicationUpdate(name=data.name), db_obj=db_obj)
            return await HttpResponseMethod.ok(
                data=ContraindicationResponse(**result.dict()).dict(),
                message=f"Contraindication {data.id} updated successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def delete(self, session: AsyncSession, contraindication_id: int):
        try:
            db_obj = await self.crud.get(session, id=contraindication_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Contraindication {contraindication_id} not found"
                )
            await self.crud.delete(session, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                message=f"Contraindication {contraindication_id} deleted successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))
