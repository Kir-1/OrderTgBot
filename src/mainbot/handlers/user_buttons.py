from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select, Result

from ..texts import profile_text, information_text, queue_text, price_text
from src.core.models import Worker, User
from src.core import database
from ..keyboards import profile_menu, accepinfo_menu
from ..states import Order

user_buttons_router = Router()


@user_buttons_router.message(F.text == "👨🏼‍💻Профиль👨🏼‍💻")
async def profile(message: Message) -> None:
    async with database.session_factory() as session:
        user = await session.get(User, {"id": message.from_user.id})

    await message.answer(
        await profile_text(user=user, user_name=message.from_user.username),
        reply_markup=await profile_menu(user.notification),
    )


@user_buttons_router.message(F.text == "❗Информация❗")
async def information(message: Message) -> None:
    async with database.session_factory() as session:
        user = await session.get(User, {"id": message.from_user.id})

    await message.answer(
        text=await information_text(
            project_manager="@akahuub",
            support="@Aputalabashuneba",
            theme="https://zelenka.guru/threads/5301100/",
        ),
        reply_markup=await accepinfo_menu() if not user.accept_info else None,
    )


@user_buttons_router.message(F.text == "🚪Очередь🚪")
async def queue(message: Message) -> None:
    async with database.session_factory() as session:
        stmt = select(Worker)
        result: Result = await session.execute(stmt)
        workers = list(result.scalars().all())

    await message.answer(text=await queue_text(workers=workers))


@user_buttons_router.message(F.text == "📈Заказать SEO📈")
async def order(message: Message, state: FSMContext) -> None:
    async with database.session_factory() as session:
        user = await session.get(User, {"id": message.from_user.id})
    if not user.accept_info:
        await message.answer(
            "<b>Для начала использования бота необходимо прочитать информацию и согласиться с правилами использования</b>"
        )
        return

    await message.answer(text=await price_text(100))
    await state.set_state(Order.vido_link)
