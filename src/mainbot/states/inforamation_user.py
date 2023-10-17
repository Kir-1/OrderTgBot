from aiogram.fsm.state import StatesGroup, State


class InformationUser(StatesGroup):
    user = State()
    change = State()
