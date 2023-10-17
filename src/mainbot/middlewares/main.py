from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from .throttling import ThrottlingMiddleware


async def register_all_middlewares(dp: Dispatcher) -> None:
    storage = RedisStorage.from_url("redis://localhost:6379:0")
    dp.message.middleware.register(ThrottlingMiddleware(storage=storage))
