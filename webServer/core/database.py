from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import Settings

settings = Settings()
engine = create_async_engine(settings.POSTGRES_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def connect_db() -> None:
    from model.base import Base
    import model.clinician              # noqa: F401
    import model.patient                # noqa: F401
    import model.measurement            # noqa: F401
    import model.objective_measurement  # noqa: F401
    import model.exercise               # noqa: F401
    import model.treatment              # noqa: F401
    import model.treatment_content      # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def disconnect_db() -> None:
    await engine.dispose()


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session