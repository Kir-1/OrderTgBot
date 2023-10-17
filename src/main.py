import asyncio
from core.models import Base, User
from core import Database, database
from mainbot import start_bot


async def startup():
    async with database.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    # asyncio.run(startup())
    start_bot()
