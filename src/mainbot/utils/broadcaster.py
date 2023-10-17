import asyncio

from src.core.models import User, Worker, Order, Admin, Status
from src.core import database
from typing import Union
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter


async def broadcast(
    bot: Bot, model: Union[User, Worker, Admin], ids: list[int], text: str = ""
) -> None:
    for id in ids:
        async with database.session_factory() as session:
            model_element = await session.get(model, {"id": id})

            notification = True
            if isinstance(model_element, User):
                notification = model_element.notification
            if notification:
                if await send_message(bot, id, text) is False:
                    model_element.is_available = False
                    session.commit()


async def send_message(bot: Bot, id: int, text: str) -> bool:
    try:
        await bot.send_message(id, text)
        return True
    except TelegramRetryAfter as ex:
        await asyncio.sleep(ex.retry_after)
        return await send_message(bot, id, text)
    except Exception as ex:
        return False
