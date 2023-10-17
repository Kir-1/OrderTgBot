from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import CommandStart
from ..texts import start_text

from ..keyboards import main_menu

from src.core import database
from src.core.models import User


user_commands_router = Router()


@user_commands_router.message(CommandStart())
async def start(message: Message) -> None:
    async with database.session_factory() as session:
        user = User(id=message.from_user.id)
        await session.merge(user)
        await session.commit()

    await message.answer(
        await start_text(project_manager="@akahuub", support="@Aputalabashuneba"),
        reply_markup=await main_menu(),
    )
