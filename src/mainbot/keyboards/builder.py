from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.core.models import Worker


async def room_menu(workers: list[Worker]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for worker in workers:
        builder.button(
            text=f"{worker.room_emoji}{worker.room_name}{worker.room_emoji} {worker.busy_spot}/{worker.all_spot} - {'свободна' if worker.busy_spot < worker.all_spot else 'занята'}",
            callback_data=f"Комната {worker.id} {'свободна' if worker.busy_spot < worker.all_spot else 'занята'}",
        )
    return builder.as_markup()
