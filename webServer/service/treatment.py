from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.httpResponseMethod import HttpResponseMethod
from crud.patient import CRUDPatient
from crud.exercise import CRUDExercise
from crud.treatment import CRUDTreatment
from crud.treatment_content import CRUDTreatmentContent
from crud.treatment_result import CRUDTreatmentResult
from schema.treatment import (
    CreateRequest, UpdateRequest,
    TreatmentCreate, TreatmentUpdate, TreatmentResponse,
    TreatmentContentCreate, TreatmentContentInput, TreatmentContentItem,
    TreatmentFullCreateRequest, TreatmentFullUpdateRequest, TreatmentFullResponse,
    TreatmentListItem,
)
from util.datetimeConverter import datetimeConverter
from util.emailSender import EmailSender
from util.qrCodeService import QRCodeService


class TreatmentService:

    def __init__(self):
        self.crud_treatment = CRUDTreatment()
        self.crud_content = CRUDTreatmentContent()
        self.crud_patient = CRUDPatient()
        self.crud_exercise = CRUDExercise()
        self.crud_result = CRUDTreatmentResult()

    async def create(self, session: AsyncSession, data: CreateRequest):
        try:
            patient = await self.crud_patient.get(session, id=data.patient_id)
            if patient is None:
                return await HttpResponseMethod.not_found(
                    message=f"Patient {data.patient_id} not found"
                )
            cur = datetimeConverter.get_current_timestamp()
            create_data = TreatmentCreate(**data.dict(), created_at=cur)
            result = await self.crud_treatment.create(session, obj_in=create_data)
            return await HttpResponseMethod.ok(
                data=TreatmentResponse(**result.dict()).dict(),
                message=f"Treatment {result.id} created successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_by_id(self, session: AsyncSession, treatment_id: int):
        try:
            result = await self.crud_treatment.get(session, id=treatment_id)
            if result is None:
                return await HttpResponseMethod.not_found(
                    message=f"Treatment {treatment_id} not found"
                )
            return await HttpResponseMethod.ok(
                data=TreatmentResponse(**result.dict()).dict(),
                message=f"Treatment {treatment_id} retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def update(self, session: AsyncSession, data: UpdateRequest):
        try:
            db_obj = await self.crud_treatment.get(session, id=data.id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Treatment {data.id} not found"
                )
            cur = datetimeConverter.get_current_timestamp()
            update_data = TreatmentUpdate(**data.dict(), updated_at=cur)
            result = await self.crud_treatment.update(session, obj_in=update_data, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                data=TreatmentResponse(**result.dict()).dict(),
                message=f"Treatment {data.id} updated successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def delete(self, session: AsyncSession, treatment_id: int):
        try:
            db_obj = await self.crud_treatment.get(session, id=treatment_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Treatment {treatment_id} not found"
                )
            await self.crud_content.delete_by_treatment_id(session, treatment_id)
            await self.crud_treatment.delete(session, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                message=f"Treatment {treatment_id} deleted successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def create_full(self, session: AsyncSession, data: TreatmentFullCreateRequest):
        try:
            patient = await self.crud_patient.get(session, id=data.patient_id)
            if patient is None:
                return await HttpResponseMethod.not_found(
                    message=f"Patient {data.patient_id} not found"
                )
            for item in data.contents:
                exercise = await self.crud_exercise.get(session, id=item.exercise_id)
                if exercise is None:
                    return await HttpResponseMethod.not_found(
                        message=f"Exercise {item.exercise_id} not found"
                    )
            cur = datetimeConverter.get_current_timestamp()
            create_data = TreatmentCreate(
                name=data.name,
                patient_id=data.patient_id,
                start_time=data.start_time,
                end_time=data.end_time,
                created_at=cur,
            )
            treatment = await self.crud_treatment.create(session, obj_in=create_data)
            content_list = []
            for item in data.contents:
                content_create = TreatmentContentCreate(
                    treatment_id=treatment.id,
                    exercise_id=item.exercise_id,
                    sets=item.sets,
                    reps=item.reps,
                    set_rest_time=item.set_rest_time,
                    date=item.date,
                )
                content = await self.crud_content.create(session, obj_in=content_create)
                content_list.append(TreatmentContentItem(**{k: v for k, v in content.dict().items() if k != "treatment_id"}))
            return await HttpResponseMethod.ok(
                data=TreatmentFullResponse(**treatment.dict(), contents=content_list).dict(),
                message=f"Treatment {treatment.id} created successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_full(self, session: AsyncSession, treatment_id: int):
        try:
            treatment = await self.crud_treatment.get(session, id=treatment_id)
            if treatment is None:
                return await HttpResponseMethod.not_found(
                    message=f"Treatment {treatment_id} not found"
                )
            contents = await self.crud_content.get_by_treatment_id(session, treatment_id)
            content_list = [TreatmentContentItem(**{k: v for k, v in c.dict().items() if k != "treatment_id"}) for c in contents]
            return await HttpResponseMethod.ok(
                data=TreatmentFullResponse(**treatment.dict(), contents=content_list).dict(),
                message=f"Treatment {treatment_id} retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def update_full(self, session: AsyncSession, data: TreatmentFullUpdateRequest):
        try:
            db_obj = await self.crud_treatment.get(session, id=data.id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Treatment {data.id} not found"
                )
            if data.contents is not None:
                for item in data.contents:
                    exercise = await self.crud_exercise.get(session, id=item.exercise_id)
                    if exercise is None:
                        return await HttpResponseMethod.not_found(
                            message=f"Exercise {item.exercise_id} not found"
                        )
            cur = datetimeConverter.get_current_timestamp()
            update_data = TreatmentUpdate(**data.dict(exclude={"contents"}), updated_at=cur)
            treatment = await self.crud_treatment.update(session, obj_in=update_data, db_obj=db_obj)
            if data.contents is not None:
                await self.crud_content.delete_by_treatment_id(session, data.id)
                content_list = []
                for item in data.contents:
                    content_create = TreatmentContentCreate(
                        treatment_id=data.id,
                        exercise_id=item.exercise_id,
                        sets=item.sets,
                        reps=item.reps,
                        set_rest_time=item.set_rest_time,
                        date=item.date,
                    )
                    content = await self.crud_content.create(session, obj_in=content_create)
                    content_list.append(TreatmentContentItem(**{k: v for k, v in content.dict().items() if k != "treatment_id"}))
            else:
                contents = await self.crud_content.get_by_treatment_id(session, data.id)
                content_list = [TreatmentContentItem(**{k: v for k, v in c.dict().items() if k != "treatment_id"}) for c in contents]
            return await HttpResponseMethod.ok(
                data=TreatmentFullResponse(**treatment.dict(), contents=content_list).dict(),
                message=f"Treatment {data.id} updated successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def delete_full(self, session: AsyncSession, treatment_id: int):
        try:
            db_obj = await self.crud_treatment.get(session, id=treatment_id)
            if db_obj is None:
                return await HttpResponseMethod.not_found(
                    message=f"Treatment {treatment_id} not found"
                )
            await self.crud_result.delete_by_treatment_id(session, treatment_id)
            await self.crud_content.delete_by_treatment_id(session, treatment_id)
            await self.crud_treatment.delete(session, db_obj=db_obj)
            return await HttpResponseMethod.ok(
                message=f"Treatment {treatment_id} deleted successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def send_email(self, session: AsyncSession, treatment_id: int):
        try:
            print(f"[send_email] start, treatment_id={treatment_id}", flush=True)

            treatment = await self.crud_treatment.get(session, id=treatment_id)
            if treatment is None:
                print(f"[send_email] treatment {treatment_id} not found", flush=True)
                return await HttpResponseMethod.not_found(
                    message=f"Treatment {treatment_id} not found"
                )
            print(f"[send_email] treatment found: {treatment.name}", flush=True)

            patient = await self.crud_patient.get(session, id=treatment.patient_id)
            if patient is None:
                print(f"[send_email] patient {treatment.patient_id} not found", flush=True)
                return await HttpResponseMethod.not_found(
                    message=f"Patient {treatment.patient_id} not found"
                )
            if not patient.email:
                print(f"[send_email] patient has no email", flush=True)
                return await HttpResponseMethod.bad_request(
                    message="個案尚未設定 email"
                )
            print(f"[send_email] patient email={patient.email}", flush=True)

            contents = await self.crud_content.get_by_treatment_id(session, treatment_id)
            plan_data = {
                "id": treatment.id,
                "name": treatment.name,
                "patient_id": treatment.patient_id,
                "start_time": treatment.start_time,
                "end_time": treatment.end_time,
                "contents": [
                    {k: v for k, v in c.dict().items() if k != "treatment_id"}
                    for c in contents
                ],
            }

            print(f"[send_email] building email message", flush=True)
            sender = EmailSender()
            sender.build_message(
                receiver_email=patient.email,
                subject=f"治療計畫：{treatment.name}",
            )
            sender.attach_body(f"您好，\n\n請查收附件中的治療計畫「{treatment.name}」。\n\n謝謝！")
            sender.attach_json(plan_data)

            print(f"[send_email] calling aiosmtplib.send ...", flush=True)
            await sender.send()
            print(f"[send_email] email sent successfully", flush=True)

            return await HttpResponseMethod.ok(
                message=f"治療計畫已成功寄送至 {patient.email}"
            )
        except Exception as e:
            print(f"[send_email] ERROR: {type(e).__name__}: {e}", flush=True)
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_qrcode(self, session: AsyncSession, treatment_id: int):
        try:
            treatment = await self.crud_treatment.get(session, id=treatment_id)
            if treatment is None:
                return await HttpResponseMethod.not_found(
                    message=f"Treatment {treatment_id} not found"
                )
            contents = await self.crud_content.get_by_treatment_id(session, treatment_id)
            plan_data = {
                "id": treatment.id,
                "name": treatment.name,
                "patient_id": treatment.patient_id,
                "start_time": treatment.start_time,
                "end_time": treatment.end_time,
                "contents": [
                    {k: v for k, v in c.dict().items() if k != "treatment_id"}
                    for c in contents
                ],
            }
            qr_service = QRCodeService()
            qr_service.generate_qrcode(data=plan_data)
            return FileResponse(
                path=str(qr_service._output_path),
                media_type="image/png",
                filename=f"treatment_{treatment_id}_qrcode.png",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))

    async def get_by_patient_id(self, session: AsyncSession, patient_id: int):
        try:
            patient = await self.crud_patient.get(session, id=patient_id)
            if patient is None:
                return await HttpResponseMethod.not_found(
                    message=f"Patient {patient_id} not found"
                )
            treatments = await self.crud_treatment.get_multi(session, patient_id=patient_id)
            result = []
            for t in treatments:
                contents = await self.crud_content.get_by_treatment_id(session, t.id)
                content_list = [TreatmentContentItem(**{k: v for k, v in c.dict().items() if k != "treatment_id"}) for c in contents]
                result.append(TreatmentListItem(
                    id=t.id,
                    name=t.name,
                    start_time=t.start_time,
                    end_time=t.end_time,
                    contents=content_list,
                ).dict())
            return await HttpResponseMethod.ok(
                data=result,
                message=f"Treatments for patient {patient_id} retrieved successfully",
            )
        except Exception as e:
            return await HttpResponseMethod.internal_server_error(message=str(e))
