from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from sqlalchemy import Result, select

from src.core.models import Order
from src.core import database
from ..utils import get_video_seo, get_video_information
from ..texts import check_seo_text

common_callbacks_router = Router()


@common_callbacks_router.callback_query(F.data.startswith("Проверка сео"))
async def check_seo(callback_query: CallbackQuery) -> None:
    _, _, video_id, user_id = callback_query.data.split(" ")
    photo = callback_query.message.photo
    async with database.session_factory() as session:
        stmt = select(Order).where(Order.id == video_id)
        result: Result = await session.execute(stmt)
        orders = result.scalars().all()

    if not orders:
        await callback_query.message.delete()
        return

    _, video_tags, video_title, video_description, _ = await get_video_information(
        video_id=video_id
    )
    video_seo = await get_video_seo(
        tags=video_tags, title=video_title, description=video_description
    )
    keyboad = callback_query.message.reply_markup
    try:
        if not photo:
            await callback_query.message.edit_text(
                text=await check_seo_text(
                    url=orders[0].url, seo=video_seo, tags=video_tags
                ),
                reply_markup=keyboad,
            )
        else:
            await callback_query.message.edit_caption(
                caption=await check_seo_text(
                    url=orders[0].url, seo=video_seo, tags=video_tags
                ),
                reply_markup=keyboad,
            )
    except TelegramBadRequest as ex:
        await callback_query.answer("")
        return
