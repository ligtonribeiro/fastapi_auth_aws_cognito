import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mangum import Mangum

from app.controllers import main_router
from app.infrastructure.config.init_db import init_db

root_path = os.getenv('ENV', default='')
app = FastAPI(
    title='Authentication API example',
    version='0.0.1',
    description='Example of a user registration and authentication API with AWS Cognito',
    root_path=f'/{root_path}'
)


# @app.on_event('startup')
# async def start_db():
#     await init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)

handler = Mangum(app)
