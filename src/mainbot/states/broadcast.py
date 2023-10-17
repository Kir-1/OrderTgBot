from aiogram.fsm.state import StatesGroup, State


class Broadcast(StatesGroup):
    text = State()
    agree = State()
