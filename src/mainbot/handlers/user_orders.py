import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy import Result

from ..texts import video_response_text, worker_order_text
from src.core.models import User, Worker, Order
from src.core import database
from ..keyboards import room_menu, order_menu
from ..states import Order as Order_state
from ..utils import (
    broadcast,
    get_video_url,
    get_video_information,
    get_channel_information,
    get_channel_id,
    get_video_seo,
)

user_order_router = Router()


@user_order_router.message(F.text, Order_state.vido_link)
async def order_video_url(message: Message, state: FSMContext) -> None:
    video_url, video_id = await get_video_url(message.text)
    if video_url is None:
        await message.answer("Неверная ссылка")
        await state.clear()
        return

    async with database.session_factory() as session:
        stmt = select(Worker).where(Worker.status == True)
        result: Result = await session.execute(stmt)
        workers = list(result.scalars().all())

    await message.answer(
        "Выберите свободную комнату😳", reply_markup=await room_menu(workers=workers)
    )
    await state.update_data(video_id=video_id)
    await state.update_data(url=video_url)
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(Order_state.room)


@user_order_router.message(Order_state.room)
async def order_room(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Вы не выбрали свободную комнату😢!\nВозможно свободных комнат нет, попробуйте позже⏳"
    )
    await state.clear()
    return


@user_order_router.callback_query(F.data.startswith("Комната"))
async def order_room(callback_query: CallbackQuery, state: FSMContext) -> None:
    worker_id = callback_query.data.split(" ")[1]
    is_free = True if callback_query.data.split(" ")[2] == "свободна" else False

    if not is_free:
        await callback_query.answer(
            "Вы выбрали занятую комнату😢!\nВозможно свободных комнат нет, попробуйте позже⏳",
            show_alert=True,
        )
        await callback_query.message.delete()
        await state.clear()
        return

    async with database.session_factory() as session:
        user = await session.get(User, {"id": (await state.get_data())["user_id"]})

    if user.balance < 100:
        await callback_query.answer(
            text=f"Вам не хватает {100 - user.balance}", show_alert=True
        )
        await callback_query.message.delete()
        await state.clear()
        return

    async with database.session_factory() as session:
        worker = await session.get(Worker, {"id": worker_id})

        worker.busy_spot += 1
        await session.commit()

    video_id = (await state.get_data())["video_id"]
    channel_id = await get_channel_id(video_id=video_id)
    (
        time_video_exist,
        video_tags,
        video_title,
        video_description,
        video_views,
    ) = await get_video_information(video_id=video_id)
    time_channel_exist, count_channel_subscriber = await get_channel_information(
        channel_id=channel_id
    )

    video_seo = await get_video_seo(
        tags=video_tags, title=video_title, description=video_description
    )
    if None in [
        video_id,
        channel_id,
        time_video_exist,
        video_tags,
        video_title,
        video_description,
        video_views,
        time_channel_exist,
        count_channel_subscriber,
        video_seo,
    ]:
        await callback_query.answer(
            "Ошибка получения информации о видео, обратитесь в техническую поддержку",
            show_alert=True,
        )
        async with database.session_factory() as session:
            worker = await session.get(Worker, {"id": worker_id})

            worker.busy_spot -= 1
            await session.commit()
        await state.clear()
        return

    await callback_query.answer("Проверка очереди и получение информации о видео")
    await callback_query.message.answer(
        await video_response_text(
            video_time=True
            if time_video_exist <= datetime.timedelta(hours=1)
            else False,
            channel_time=True
            if time_channel_exist <= datetime.timedelta(days=365 * 2)
            else False,
            channel_sub=True if count_channel_subscriber >= 500 else False,
            seo=True if video_seo > 45 else False,
        )
    )

    moneyback = all(
        [
            True if time_video_exist <= datetime.timedelta(hours=1) else False,
            True if time_channel_exist <= datetime.timedelta(days=365 * 2) else False,
            True if count_channel_subscriber >= 500 else False,
            True if video_seo > 45 else False,
        ]
    )

    await callback_query.message.delete()

    await callback_query.bot.send_message(
        chat_id=worker_id,
        text=await worker_order_text(
            moneyback=moneyback,
            url=(await state.get_data())["url"],
            user_id=user.id,
            user_name=callback_query.from_user.username,
            seo=video_seo,
            created_time=time_video_exist,
            subs=count_channel_subscriber,
            views=video_views,
            tags=video_tags,
        ),
        reply_markup=await order_menu(video_id=video_id, user_id=user.id),
    )
    async with database.session_factory() as session:
        user = await session.get(Worker, {"id": (await state.get_data())["user_id"]})
        user.balance -= 100
        await session.commit()

    async with database.session_factory() as session:
        order = Order(
            id=video_id,
            url=(await state.get_data())["url"],
            worker_id=worker_id,
            worker=worker,
            user_id=(await state.get_data())["user_id"],
            refund=moneyback,
        )

        await session.merge(order)
        await session.commit()

    await state.clear()
