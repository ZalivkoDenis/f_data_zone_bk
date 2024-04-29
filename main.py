from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.helpers import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.Begin() as conn:
        await conn.run_sync(db_helper.Base.metadata.create_all)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
