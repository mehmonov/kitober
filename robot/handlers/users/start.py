import logging

from asgiref.sync import sync_to_async
from robot.models import TelegramUser

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from const_texts import c_get_hello, c_get_hello_back, c_register
from robot.keyboards.default import make_buttons

from asgiref.sync import sync_to_async
from robot.keyboards.default.menu import menu
from robot.utils.get_user import get_user
from robot.states.search_book import SearchBook

@dp.message_handler(state="*",text='Bosh menyu')
async def info(message: types.Message):

    await message.answer("Bosh menyuga qaytamiz", reply_markup=menu)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        await get_user(message.from_user.id)
        logging.info("User already exists")
        await message.answer(
            text=c_get_hello_back(
            message.from_user.full_name),
            reply_markup=menu
        )
    except TelegramUser.DoesNotExist:
        logging.info("New user")
        await message.answer(
            text=c_get_hello(message.from_user.full_name),
            reply_markup=make_buttons([c_register])
        )

@dp.message_handler(text='Biz haqimizda 👁️')
async def info(message: types.Message):

    await message.answer("Bot haqida savollaringiz mavjud bo'lsa aloqaga chiqing. Dasturchi:  @husniddin092")


