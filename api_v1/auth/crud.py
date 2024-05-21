from fastapi import Depends, HTTPException
from sqlalchemy import select, Result, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.auth.schemas import CreateUser
from core.cipher.utils import hash_password
from core.helpers import db_helper
from core.models import User


async def get_user_by_user_email(
    user_email: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    stmt = select(User).filter(User.user_email == user_email)
    # stmt = select(User).filter(func.lower(User.user_email) == func.lower(user_email))
    # stmt = select(User).filter_by(user_email=user_email)
    result: Result = await session.execute(stmt)
    user = result.scalars().first()
    return user


async def check_user_exists_by_user_email(
    session: AsyncSession, user_email: str
) -> bool:
    return (
        await get_user_by_user_email(user_email=user_email, session=session) is not None
    )


async def create_admin_if_not_exists(
    session: AsyncSession,
) -> User:
    if (
        not (
            admin := await get_user_by_user_email(
                session=session,
                user_email="admin@ferico.by",
            )
        )
        is None
    ):
        return admin
    else:
        admin: User = User(
            user_email="admin@ferico.by",
            password_hash=hash_password("admin"),
            active=True,
            superuser=True,
        )
        session.add(admin)
        await session.commit()
        return admin


async def deactivate_user(
    user: User,
    session: AsyncSession,
) -> None:
    user.active = False
    session.add(user)
    await session.commit()
    return None


async def create_user(
    user: CreateUser,
    session: AsyncSession,
) -> User:
    if await check_user_exists_by_user_email(
        session=session,
        user_email=user.user_email,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This name {user.user_email!r} is busy. Try new name",
        )
    new_user: User = User(
        user_email=user.user_email,
        password_hash=hash_password(user.user_password),
        active=True,
        superuser=False,
    )
    session.add(new_user)
    await session.commit()
    return new_user
