from pathlib import Path
from typing import Any, Dict, Optional
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # therapistClinical/
<<<<<<< HEAD
=======
STATIC_DIR   = BASE_DIR / "webClient" / "www" / "static"
TEMPLATE_DIR = BASE_DIR / "webClient" / "www" / "template"
INDEX_HTML   = BASE_DIR / "webClient" / "www" / "index.html"
>>>>>>> origin/main
EXERCISE_JSON = BASE_DIR / "webServer" / "util" / "exercise.json"
TREATMENT_JSON = BASE_DIR / "webServer" / "util" / "treatment.json"

class Settings:
    POSTGRES_URI = os.environ.get(
        "POSTGRES_URI",
        "postgresql+asyncpg://clinical:Damn13258@localhost:5432/clinical_db"
    )
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)
    SESSION_EXPIRE_SECONDS: int = int(os.environ.get("SESSION_EXPIRE_SECONDS", 3600))
    DB_CONNECT_MAX_RETRIES: int = int(os.environ.get("DB_CONNECT_MAX_RETRIES", 10))
    DB_CONNECT_RETRY_DELAY: int = int(os.environ.get("DB_CONNECT_RETRY_DELAY", 3))