from fastapi import FastAPI

from .controllers import main_router

from app.infrastructure.config.init_db import init_db

app = FastAPI(
    title='Authentication API example',
    version='0.0.1',
    description='Example of a user registration and authentication API with AWS Cognito'
)


@app.on_event('startup')
async def start_db():
    await init_db()

app.include_router(main_router)
