from aiogram.dispatcher.filters.state import StatesGroup, State


class AddBook(StatesGroup):
    name = State()
    author = State()
    genre = State()
    desc = State()
    image = State()
