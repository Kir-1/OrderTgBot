from aiogram.fsm.state import StatesGroup, State


class Order(StatesGroup):
    vido_link = State()
    room = State()
