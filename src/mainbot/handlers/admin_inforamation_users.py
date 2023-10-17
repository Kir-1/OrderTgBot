import datetime
from copy import copy

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from src.core.models import User
from src.core import database
from ..states import InformationUser
from ..filters import IsAdmin
from ..texts import user_information_text

admin_information_user = Router()


@admin_information_user.message(F.text, InformationUser.user, IsAdmin())
async def worker_broadcast_text(message: Message, state: FSMContext) -> None:
    try:
        user = await message.bot.get_chat(chat_id=message.text)
        async with database.session_factory() as session:
            user_bd = await session.get(User, {"id": user.id})

        await message.answer(
            text=await user_information_text(
                user_id=user.id,
                user_name=user.username,
                balance=user_bd.balance,
                accept_info=user_bd.acceptinfo,
            )
        )

        await state.update_data(user=user_bd)
        await state.set_state(InformationUser.change)
    except TelegramBadRequest as ex:
        await message.answer(text="Такого пользователя не существует")
        await state.clear()
        return


@admin_information_user.message(F.text, InformationUser.change, IsAdmin())
async def worker_broadcast_text(message: Message, state: FSMContext) -> None:
    param, change = message.text.split(" ")
    async with database.session_factory() as session:
        user = await session.get(User, {"id": (await state.get_data())["user"].id})
        try:
            user.balance = change if param == "Balance" else user.balance
            user.accept_info = change if param == "Accept" else user.accept_info
            await message.answer(f"Параметр {param} успешно изменён")
        except ValueError:
            await message.answer(f"Параметр {param} нельзя изменить так")
        finally:
            await state.clear()
            await session.commit()
            return
