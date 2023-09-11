from fastapi import FastAPI

from .controllers import main_router

app = FastAPI(
    title='Authentication API example',
    version='0.0.1',
    description='Example of a user registration and authentication API with AWS Cognito'
)

app.include_router(main_router)
