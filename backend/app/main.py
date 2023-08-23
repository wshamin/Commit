from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from .api.routes.users import router

app = FastAPI(docs_url="/api/docs")

origins = [
    "http://127.0.0.1:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api", tags=["users"])

# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="Your API",
#         version="1.0.0",
#         description="Your API description",
#         routes=app.routes,
#     )
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi