from aiogram.fsm.state import StatesGroup, State


class Payment(StatesGroup):
    input_amount = State()
