from fastapi import FastAPI
from .api.routes.users import router

app = FastAPI()

app.include_router(router, prefix="/api", tags=["users"])
