from datetime import timedelta

from .schemas import UserSchema, UserCredentials
from core.cipher.utils import encode_jwt, decode_jwt
from core.config import settings

TOKEN_TYPE_FIELD = "type"
TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {
        TOKEN_TYPE_FIELD: token_type,
    }
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": user.user_email,
        "username": user.user_email,
    }
    return create_jwt(
        token_type=TOKEN_TYPE_ACCESS,
        token_data=jwt_payload,
        # expire_minutes=settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta=timedelta(days=15),
    )


def create_refresh_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": user.user_email,
    }
    return create_jwt(
        token_type=TOKEN_TYPE_REFRESH,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )
