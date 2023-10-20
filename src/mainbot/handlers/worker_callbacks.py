from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import select, Result

from src.core.models import User, Worker, Order, Admin, Status
from src.core import database
from ..keyboards import order_control_menu, order_check_seo_menu, worker_menu
from ..texts import (
    worker_order_access_text,
    user_waiting_order_text,
    log_order_text,
    report_order_text,
    room_free_text,
)
from ..utils import take_photo, broadcast
from ..states import Broadcast, InformationUser

from src.core.config import settings


worker_callbacks_router = Router()


@worker_callbacks_router.callback_query(
    F.data.startswith("Заказ принят") | F.data.startswith("Заказ отклонён")
)
async def order(callback_query: CallbackQuery) -> None:
    _, choice, video_id, user_id = callback_query.data.split(" ")
    choice = True if choice == "принят" else False

    if not choice:
        async with database.session_factory() as session:
            user = await session.get(User, {"id": user_id})
            worker = await session.get(Worker, {"id": callback_query.from_user.id})
            current_order = await session.get(Order, {"id": video_id})
            user.balance += 100
            worker.busy_spot -= 1
            await session.delete(current_order)
            await session.commit()

        await callback_query.bot.send_message(
            chat_id=user_id,
            text="Данная комната отказалась от  вашего заказа, вам возвращено 100 рублей",
        )
        await callback_query.answer("Вы отказались от заказа")
        await callback_query.message.delete()
        return

    async with database.session_factory() as session:
        user = await session.get(User, {"id": user_id})
        worker = await session.get(Worker, {"id": callback_query.from_user.id})
        current_order = await session.get(Order, {"id": video_id})
        current_order.status = Status.RECEIVED
        await session.commit()

    await callback_query.message.answer(
        text=await worker_order_access_text(
            order_id=current_order.id,
            order_url=current_order.url,
            user_id=int(user_id),
            user_name=(await callback_query.bot.get_chat(user_id)).username,
        ),
        reply_markup=await order_control_menu(
            video_id=current_order.id,
            user_id=int(user_id),
            moneyback=current_order.refund
            and (user.count_fail_orders < user.max_count_fail_orders),
        ),
    )
    await callback_query.message.delete()
    photo = await take_photo()
    await callback_query.bot.send_photo(
        chat_id=user_id,
        caption=await user_waiting_order_text(
            photo_name=photo.filename.split(".")[0], video_id=video_id
        ),
        photo=photo,
        reply_markup=await order_check_seo_menu(video_id=video_id, user_id=user_id),
    )

    with open("seolog.txt", "a", encoding="utf-8") as file:
        file.write(
            await log_order_text(
                state="waiting",
                worker_id=worker.id,
                worker_name=worker.room_name,
                video_id=video_id,
            )
        )

    await callback_query.answer()


@worker_callbacks_router.callback_query(
    F.data.startswith("Заказ успех") | F.data.startswith("Заказ неудача")
)
async def order_access(callback_query: CallbackQuery) -> None:
    _, choice, video_id, user_id = callback_query.data.split(" ")
    choice = True if choice == "успех" else False
    async with database.session_factory() as session:
        user = await session.get(User, {"id": user_id})
        worker = await session.get(Worker, {"id": callback_query.from_user.id})
        current_order = await session.get(Order, {"id": video_id})

    if not choice:
        with open("seolog.txt", "a", encoding="utf-8") as file:
            file.write(
                await log_order_text(
                    state="failed",
                    worker_id=worker.id,
                    worker_name=worker.room_name,
                    video_id=video_id,
                )
            )
        await callback_query.bot.send_message(
            chat_id=user_id,
            text=f"К сожалению Ваш заказ #{video_id} не был успешно выполнен,"
            f"Вам возвращено 100 рублей ",
        )

        async with database.session_factory() as session:
            stmt = select(User).where(User.is_available == True)
            result: Result = await session.execute(stmt)
            users = result.scalars().all()

        await broadcast(
            bot=callback_query.bot,
            model=User,
            ids=users,
            text=await room_free_text(worker=worker),
        )

        async with database.session_factory() as session:
            await session.delete(current_order)
            user.count_fail_orders += 1
            user.balance += 100
            worker.busy_spot -= 1
            await session.commit()

        await callback_query.message.delete()

    with open("seolog.txt", "a", encoding="utf-8") as file:
        file.write(
            await log_order_text(
                state="success",
                worker_id=worker.id,
                worker_name=worker.room_name,
                video_id=video_id,
            )
        )

    await callback_query.bot.send_message(
        chat_id=user_id, text=f"Ваш заказ #{video_id} был успешно выполнен"
    )

    await callback_query.bot.send_message(
        chat_id=settings.ID_REPORT_GROUP,
        text=await report_order_text(
            video_id=video_id, worker=worker, moneyback=current_order.refund
        ),
    )
    await callback_query.bot.send_message(
        chat_id=settings.ID_REPORT_ADMIN, text=f"/seo {current_order.url}"
    )

    async with database.session_factory() as session:
        stmt = select(User.id).where(User.is_available == True)
        result: Result = await session.execute(stmt)
        users = result.scalars().all()
        stmt = select(Admin.id).where(Admin.is_available == True)
        result: Result = await session.execute(stmt)
        admins = result.scalars().all()

    await broadcast(
        bot=callback_query.bot,
        model=Admin,
        ids=admins,
        text=await report_order_text(
            video_id=video_id, worker=worker, moneyback=current_order.refund
        ),
    )

    await broadcast(
        bot=callback_query.bot,
        model=User,
        ids=users,
        text=await room_free_text(worker=worker),
    )

    async with database.session_factory() as session:
        await session.delete(current_order)

        user.count_fail_orders = 0
        user.count_orders += 1
        worker.busy_spot -= 1
        await session.commit()

    await callback_query.message.delete()


@worker_callbacks_router.callback_query(F.data == "Работа")
async def worker_work(callback_query: CallbackQuery) -> None:
    async with database.session_factory() as session:
        worker = await session.get(Worker, {"id": callback_query.from_user.id})
        worker.status = not worker.status
        await session.commit()

    models = [worker]

    await callback_query.message.edit_reply_markup(
        reply_markup=await worker_menu(models=models)
    )

    await callback_query.answer()


@worker_callbacks_router.callback_query(F.data == "Баланс воркера")
async def worker_balance(callback_query: CallbackQuery) -> None:
    async with database.session_factory() as session:
        worker = await session.get(Worker, {"id": callback_query.from_user.id})

    await callback_query.message.answer(text=f"Ваш баланс {worker.balance} рублей")
    await callback_query.answer("")
