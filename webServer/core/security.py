import hashlib
import hmac
import secrets

from core.config import Settings

settings = Settings()


class Security:

    @staticmethod
    def hash_password(password: str) -> str:
        salt = secrets.token_hex(16)
        pw_hash = hashlib.pbkdf2_hmac(
            'sha256', password.encode('utf-8'),
            salt.encode('utf-8'), iterations=260_000
        )
        return f"{salt}:{pw_hash.hex()}"

    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        try:
            salt, pw_hash = stored_hash.split(':', 1)
        except ValueError:
            return False
        new_hash = hashlib.pbkdf2_hmac(
            'sha256', password.encode('utf-8'),
            salt.encode('utf-8'), iterations=260_000
        )
        return hmac.compare_digest(new_hash.hex(), pw_hash)

    @staticmethod
    async def create_session(redis, clinician_id: int) -> str:
        session_id = secrets.token_urlsafe(32)
        await redis.pool.set(
            f"session:{session_id}",
            str(clinician_id),
            ex=settings.SESSION_EXPIRE_SECONDS,
        )
        return session_id

    @staticmethod
    async def delete_session(redis, session_id: str) -> None:
        await redis.pool.delete(f"session:{session_id}")
