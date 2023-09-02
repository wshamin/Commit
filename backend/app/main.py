from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes.users import router as user_router 
from .api.routes.trainings import router as training_router
from .api.routes.uploads import router as uploads_router

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

origins = [
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(training_router, prefix="/api", tags=["trainings"])
app.include_router(uploads_router, prefix="/api", tags=["uploads"])