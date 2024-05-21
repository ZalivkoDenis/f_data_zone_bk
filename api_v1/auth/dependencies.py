from fastapi import Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import User
from . import crud
from .schemas import UserCredentials
from .utils import (
    TOKEN_TYPE_ACCESS,
    TOKEN_TYPE_REFRESH,
    TOKEN_TYPE_FIELD,
)

from core.helpers import db_helper
from core.cipher import auth_utils

# Используется для проверки токена Bearer в заголовке.
# Соответственно, токен должен находиться в заголовке Authorization с префиксом Bearer.
http_bearer = HTTPBearer(auto_error=False)
#
# oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
#     tokenUrl="/api/v1/auth/login",
# )


async def validate_auth_user(
    credentials: UserCredentials,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    # Заранее готовим ошибку, которую по необходимости будем вызывать.
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    if (
        user := await crud.get_user_by_user_email(
            session=session, user_email=credentials.user_email
        )
    ) is None:
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=credentials.password,
        hashed_password=user.password_hash,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    # token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        token = credentials.credentials
    except AttributeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized! Access denied!",
        )

    try:
        payload = auth_utils.decode_jwt(  # 3
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
        )
    return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_user_by_token_sub(
    payload: dict,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    user_email: str | None = payload.get("sub")
    user = await crud.get_user_by_user_email(user_email=user_email, session=session)
    if not user is None:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


# async def get_auth_user_from_token_of_type(token_type: str) -> User:
#     async def get_auth_user_from_token(
#         payload: dict = Depends(get_current_token_payload),
#     ) -> User:
#         validate_token_type(payload, token_type)
#         return await get_user_by_token_sub(payload)
#
#     return await get_auth_user_from_token()


# class UserGetterFromToken:
#     def __init__(self, token_type: str):
#         self.token_type = token_type
#
#     def __call__(
#         self,
#         payload: dict = Depends(get_current_token_payload),
#     ):
#         validate_token_type(payload, self.token_type)
#         print("*" * 80)
#         print(payload)
#         print("*" * 80)
#         return get_user_by_token_sub(payload)


# get_current_auth_user = get_auth_user_from_token_of_type(TOKEN_TYPE_ACCESS)
# get_current_auth_user_for_refresh = UserGetterFromToken(TOKEN_TYPE_REFRESH)


async def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    validate_token_type(payload, TOKEN_TYPE_REFRESH)
    user: User = await get_user_by_token_sub(
        payload=payload,
        session=session,
    )
    return user


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    validate_token_type(payload, TOKEN_TYPE_ACCESS)
    user: User = await get_user_by_token_sub(payload=payload, session=session)  # 2
    return user


async def get_current_active_auth_user(
    # user: User = Depends(UserGetterFromToken(TOKEN_TYPE_ACCESS)),
    user: User = Depends(get_current_auth_user),
) -> User:
    if user.active:  # 1
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Inactive user",
    )


async def check_auth_user_to_rights(
    user: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    if user is None:
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user


async def user_is_superuser(
    user: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied! Only for Admin!",
    )
    if (user is None) or (not user.superuser):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user
