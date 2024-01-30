from aiogram.dispatcher.filters.state import StatesGroup, State


class SearchBook(StatesGroup):
    name = State()
    result = State()
    product = State()