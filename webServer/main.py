from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

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
from core.config import STATIC_DIR
from core.database import connect_db, disconnect_db
from core.redis import Redis
from service.exercise import ExerciseService

redis = Redis()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis.create_redis_pool()
    app.state.redis = redis
    await connect_db()
    await ExerciseService().seed_exercises()
    yield
    await disconnect_db()
    await redis.close_redis_pool()


app = FastAPI(title="TherapistClinical API", lifespan=lifespan)

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
