import subprocess
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

load_dotenv()

from controller.auth import router as auth_router
from controller.clinician import router as clinician_router
from controller.patient import router as patient_router
from controller.measurement import router as measurement_router
from controller.objective_measurement import router as objective_measurement_router
from controller.template import router as template_router
from controller.exercise import router as exercise_router
from controller.treatment import router as treatment_router
from controller.treatment_result import router as treatment_result_router
from controller.contraindication import router as contraindication_router
from core.config import STATIC_DIR
from core.database import connect_db, disconnect_db, engine
from core.redis import Redis
from service.exercise import ExerciseService
from service.contraindication import ContraindicationService

redis = Redis()


async def run_migrations() -> None:
    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT to_regclass('public.alembic_version')")
        )
        alembic_exists = result.scalar() is not None

    if not alembic_exists:
        subprocess.run(["alembic", "stamp", "head"], check=True)
    else:
        subprocess.run(["alembic", "upgrade", "head"], check=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis.create_redis_pool()
    app.state.redis = redis
    await connect_db()
    await ExerciseService().seed_exercises()
    await ContraindicationService().seed_contraindications()
    await run_migrations()
    yield
    await disconnect_db()
    await redis.close_redis_pool()


app = FastAPI(title="TherapistClinical API", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(template_router)
app.include_router(auth_router)
app.include_router(clinician_router)
app.include_router(patient_router)
app.include_router(measurement_router)
app.include_router(objective_measurement_router)
app.include_router(exercise_router)
app.include_router(treatment_router)
app.include_router(treatment_result_router)
app.include_router(contraindication_router)
