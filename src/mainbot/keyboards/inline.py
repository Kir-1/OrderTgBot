from typing import Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.core.models import Admin, Worker


async def profile_menu(notification: bool) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Пополнить баланс", callback_data="Пополнить баланс"
            ),
            InlineKeyboardButton(
                text=f"Уведомления: {'✅' if notification else '❌'}",
                callback_data=f"Уведомления {'✅' if notification else '❌'}",
            ),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def accepinfo_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Принять правила", callback_data="Принять правила")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def payment_menu(pay_id: str, url: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Оплатить", url=url),
            InlineKeyboardButton(
                text="Проверить оплату", callback_data=f"Проверить оплату {pay_id}"
            ),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def order_menu(video_id: str, user_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Принять", callback_data=f"Заказ принят {video_id} {user_id}"
            ),
            InlineKeyboardButton(
                text="Отклонить", callback_data=f"Заказ отклонён {video_id} {user_id}"
            ),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def order_control_menu(
    video_id: str, user_id: int, moneyback: bool
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Обновить SEO", callback_data=f"Проверка сео {video_id} {user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Выполнен", callback_data=f"Заказ успех {video_id} {user_id}"
            ),
            InlineKeyboardButton(
                text="Невыполнен", callback_data=f"Заказ неудача {video_id} {user_id}"
            ),
        ]
        if moneyback
        else [
            InlineKeyboardButton(
                text="Выполнен", callback_data=f"Заказ успех {video_id} {user_id}"
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def order_check_seo_menu(video_id: str, user_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Проверить seo", callback_data=f"Проверка сео {video_id} {user_id}"
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def worker_menu(model: Union[Admin, Worker]) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{'Работать' if not model.is_available else 'Не работать'}",
                callback_data="Работа",
            ),
            InlineKeyboardButton(
                text="Проверить баланс", callback_data="Баланс воркера"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Информация о пользователе",
                callback_data="Информация о пользователе",
            ),
            InlineKeyboardButton(text="Рассылка", callback_data="Рассылка"),
        ]
        if isinstance(model, Admin)
        else [],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def agree_broadcast_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Подтвердить", callback_data="Рассылка Подтвердить"
            ),
            InlineKeyboardButton(text="Отметить", callback_data="Рассылка Отметить"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
