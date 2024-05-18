import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from core.helpers import db_helper


async def demo_crud(session: AsyncSession): ...


async def main():
    async with db_helper.session_factory() as session:
        await demo_crud(session)


if __name__ == "__main__":
    asyncio.run(main())
