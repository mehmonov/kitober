from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegister(StatesGroup):
    phone_number = State()
    full_name = State()
    location = State()