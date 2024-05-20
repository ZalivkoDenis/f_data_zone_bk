from fastapi import Depends
from sqlalchemy import select, Result, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.cipher.utils import hash_password
from core.models import User


async def get_user_by_user_email(session: AsyncSession, user_email: str) -> User:
    stmt = select(User).filter(func.lower(user_email) == func.lower(User.user_email))
    result: Result = await session.execute(stmt)
    return result.scalars().first()


async def check_user_exists_by_user_email(
    session: AsyncSession, user_email: str
) -> bool:
    return await get_user_by_user_email(session, user_email) is not None


async def create_admin_if_not_exists(
    session: AsyncSession,
) -> User:
    if not (admin := await get_user_by_user_email(session, "admin@ferico.by")) is None:
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
