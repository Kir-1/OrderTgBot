from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from src.core.models import User
from src.core import database
from ..keyboards import profile_menu
from ..states import Payment

user_callbacks_router = Router()


@user_callbacks_router.callback_query(F.data.startswith("Уведомления"))
async def notification(callback_query: CallbackQuery) -> None:
    async with database.session_factory() as session:
        user = await session.get(User, {"id": callback_query.from_user.id})

        notification_state = True if callback_query.data.split(" ")[1] == "✅" else False
        if user.notification == notification_state:
            user.notification = not user.notification

            await callback_query.message.edit_reply_markup(
                reply_markup=await profile_menu(user.notification)
            )

        await callback_query.answer(text="")
        await session.commit()


@user_callbacks_router.callback_query(F.data == "Пополнить баланс")
async def notification(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.answer("Введите сумму пополнения")
    await state.set_state(Payment.input_amount)
    await callback_query.answer(text="")


@user_callbacks_router.callback_query(F.data == "Принять правила")
async def notification(callback_query: CallbackQuery) -> None:
    async with database.session_factory() as session:
        user = await session.get(User, {"id": callback_query.from_user.id})
        user.accept_info = True
        await session.commit()
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer(
        text="Вы успешно приняли правила использования бота SeoHub", show_alert=True
    )
