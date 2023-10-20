from aiogram import Router, F
from aiogram.filters import or_f
from aiogram.types import Message
from sqlalchemy import select, Result

from src.core.models import User, Worker, Order, Admin, Status
from src.core import database
from ..keyboards import worker_menu
from ..filters import IsWorker, IsAdmin

worker_commands_router = Router()


@worker_commands_router.message(F.text == "/menu", or_f(IsWorker(), IsAdmin()))
async def admin(message: Message) -> None:
    async with database.session_factory() as session:
        stmt = select(Worker).where(Worker.id == message.from_user.id)
        result: Result = await session.execute(stmt)
        workers = result.scalars().all()

        stmt = select(Admin).where(Admin.id == message.from_user.id)
        result: Result = await session.execute(stmt)
        admins = result.scalars().all()

    models = [el for el in workers] + [el for el in admins]

    await message.answer(
        "Меню администратора",
        reply_markup=await worker_menu(models=models),
    )
