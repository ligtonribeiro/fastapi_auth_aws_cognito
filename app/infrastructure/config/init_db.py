import motor.motor_asyncio

from beanie import init_beanie

from app.infrastructure.schema.user import UserSchema


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://root:root@localhost:27017/")
    await init_beanie(database=client['users_db'], document_models=[UserSchema])
