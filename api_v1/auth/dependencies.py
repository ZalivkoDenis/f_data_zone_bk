from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from . import crud
from .schemas import UserCredentials
from core.helpers import db_helper

from core.cipher import auth_utils


async def validate_auth_user(
    credentials: UserCredentials,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    # Заранее готовим ошибку, которую по необходимости будем вызывать.
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    if (
        user := await crud.get_user_by_user_email(session, credentials.user_email)
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
