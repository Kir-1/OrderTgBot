import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select, Result

from src.core.models import User
from src.core import database
from ..keyboards import agree_broadcast_menu
from ..states import Broadcast, InformationUser
from ..utils import broadcast
from ..filters import IsAdmin

admin_broadcast_router = Router()


@admin_broadcast_router.message(F.text, Broadcast.text, IsAdmin())
async def worker_broadcast_text(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    await message.answer(
        f"Потвердите рассылку текста ниже:\n {message.text}",
        reply_markup=await agree_broadcast_menu(),
    )
    await state.set_state(Broadcast.agree)


@admin_broadcast_router.callback_query(
    F.data.in_(["Рассылка Подтвердить", "Рассылка Отметить"]),
    Broadcast.agree,
    IsAdmin(),
)
async def worker_broadcast(callback_query: CallbackQuery, state: FSMContext) -> None:
    _, agree = callback_query.data.split(" ")
    agree = True if agree == "Подтвердить" else False
    if not agree:
        await callback_query.message.delete()

    async with database.session_factory() as session:
        stmt = select(User.id).where(User.is_available == True)
        result: Result = await session.execute(stmt)
        users = result.scalars().all()
        users = await session.query(User).filter(User.id == True)

    await broadcast(
        bot=callback_query.bot,
        model=User,
        ids=users,
        text=(await state.get_data())["text"],
    )

    await state.clear()
    await callback_query.message.delete()
    await callback_query.answer("")
