from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from ..states import InformationUser, Broadcast
from ..filters import IsAdmin

admin_callbacks_router = Router()


@admin_callbacks_router.callback_query(F.data == "Рассылка")
async def worker_broadcast(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.answer("Напишите текст для рассылки")
    await state.set_state(Broadcast.text)
    await callback_query.answer("")


@admin_callbacks_router.callback_query(F.data == "Информация о пользователе", IsAdmin())
async def worker_balance(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.answer(text=f"Введи id пользователя:")
    await callback_query.answer("")
    await state.set_state(InformationUser.user)
