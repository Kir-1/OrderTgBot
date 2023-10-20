from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy import select, Result

from src.core.models import User, Worker, Order, Admin, Status
from src.core import database


class IsWorker(Filter):
    async def __call__(self, message: Message) -> bool:
        async with database.session_factory() as session:
            stmt = select(Worker)
            result: Result = await session.execute(stmt)
            return (
                True
                if str(message.from_user.id) in [el.id for el in result.scalars().all()]
                else False
            )
