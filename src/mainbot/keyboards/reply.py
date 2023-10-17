from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def main_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text="👨🏼‍💻Профиль👨🏼‍💻"),
            KeyboardButton(text="📈Заказать SEO📈"),
        ],
        [
            KeyboardButton(text="❗Информация❗"),
            KeyboardButton(text="🚪Очередь🚪"),
        ]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard,
                               input_field_placeholder="Выберите действие из меню",
                               selective=True,
                               resize_keyboard=True)
