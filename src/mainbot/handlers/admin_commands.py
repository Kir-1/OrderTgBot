from aiogram import Router, F
from aiogram.filters import or_f
from aiogram.types import Message
from sqlalchemy import select, Result

from src.core.models import User
from ..keyboards import worker_menu
from ..filters import IsWorker, IsAdmin
from ..utils import CrystalpayKassa
from ..texts import admin_info_text
from src.core import database

admin_commands_router = Router()


@admin_commands_router.message(F.text == "/info", IsAdmin())
async def admin(message: Message) -> None:
    async with database.session_factory() as session:
        stmt = select(User).where(User.is_available == True)
        result: Result = await session.execute(stmt)
        users = result.scalars().all()
    info: dict = CrystalpayKassa().get_info()
    rub: dict = CrystalpayKassa().get_ticker(
        [value["currency"] for (key, value) in info.items()]
    )["currencies"]

    for coin, coin_info in info.items():
        coin_info["amount_rub"] = (
            coin_info["amount"] * rub[coin_info["currency"]]["price"]
        )

    await message.answer(text=await admin_info_text(users=users, info=info))
    return
