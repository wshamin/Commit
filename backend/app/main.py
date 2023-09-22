from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes.common.users import router as user_router 
from .api.routes.common.trainings import router as training_router
from .api.routes.common.uploads import router as upload_router
from .api.routes.common.lessons import router as lesson_router
from .api.routes.admin.trainings import router as admin_training_router
from .api.routes.admin.users import router as admin_user_router

app = FastAPI(docs_url='/api/docs', openapi_url='/api/openapi.json')

origins = [
    'http://127.0.0.1:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['Content-Range', 'Date', 'Server', 'Transfer-Encoding']
)

app.include_router(user_router, prefix='/api/user', tags=['Regular users'])
app.include_router(training_router, prefix='/api/training', tags=['Trainings'])
# app.include_router(upload_router, prefix='/api', tags=['uploads'])
# app.include_router(lesson_router, prefix='/api', tags=['lessons'])
app.include_router(admin_training_router, prefix='/api/admin/training', tags=['Admin functions for trainings'])
app.include_router(admin_user_router, prefix='/api/admin/user', tags=['Admin functions for users'])