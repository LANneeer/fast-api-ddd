from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.config import Base, engine
from app.gateway.routers import user_router, auth_router

app = FastAPI(title="ioka-test")

app.include_router(user_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Currency Transfer API",
        version="1.0.0",
        description="JWT auth enabled",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
