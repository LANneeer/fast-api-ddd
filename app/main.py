from fastapi import FastAPI
from app.config import Base, engine
from app.gateway.routers import user_router

app = FastAPI(title="ioka-test")

app.include_router(user_router, prefix="/users")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
