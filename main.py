from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

from core.helpers import db_helper
from api_v1 import router as api_v1_router

from core.config import settings
from api_v1.auth.crud import create_admin_if_not_exists


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаёт admin@ferico.by с дефолтным паролем "admin", если база пустая.
    # Пароль необходимо сразу поменять.
    # async with db_helper.session_factory() as session:
    #     await create_admin_if_not_exists(session)
    #     await session.close()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=api_v1_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Определяем точку входа в приложение
# - Но это совсем не обязательно, т.к. PyCharm прекрасно работает с Uvicorn в debug режиме
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)
