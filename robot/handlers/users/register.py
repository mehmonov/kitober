import logging

from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError


from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from const_texts import *
from robot.keyboards.default.menu import menu
from robot.models import TelegramUser
from robot.states import UserRegister
from robot.keyboards.default import make_buttons, contact_request_button


@dp.message_handler(text=c_register)
async def register(message: types.Message):
    await UserRegister.phone_number.set()
    await message.answer(
        text=c_input_phone_number,
        reply_markup=contact_request_button
    )


@dp.message_handler(state=UserRegister.phone_number, content_types='contact')
async def register(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    if not phone_number.startswith("+"):
        phone_number = "+" + phone_number

    # user = await TelegramUser.objects.filter(phone_number=phone_number).afirst()

    await UserRegister.next()
    await message.answer(
        text=c_input_full_name,
        reply_markup=make_buttons(
            words=[message.from_user.full_name, c_cancel]

        )
    )

    await state.update_data(phone_number=phone_number)


@dp.message_handler(state=UserRegister.full_name)
async def register(message: types.Message, state: FSMContext):
    await UserRegister.next()
    await message.answer(
        text=c_input_location,
        reply_markup=make_buttons(
            words=[c_cancel],
    
        )
    )
    await state.update_data(full_name=message.text)




@dp.message_handler(state=UserRegister.location)
async def register(message: types.Message, state: FSMContext):

    user_info = await state.get_data()

    try:
        await TelegramUser.objects.acreate(
            full_name=user_info.get('full_name'),
            username=message.from_user.username,
            chat_id=message.from_user.id,
            phone_number=user_info.get('phone_number'),
            location = message.text
        )
        print(type(message.from_user.id))
        
        # await TelegramUser.objects.aget(chat_id=message.from_user.id)
        
        # await sync_to_async(telegram_user.set_user)(user)
        await message.answer(
            text=c_successfully_register,
            reply_markup=menu
        )
    except IntegrityError as e:
        error_message = str(e)
        if 'UNIQUE constraint failed' in error_message:
            await message.answer(
                text='xato',
                reply_markup=make_buttons([c_register])
            )
        else:
            await message.answer(
                text=c_registeration_failed,
                reply_markup=make_buttons([c_register])
            )

    await message.delete()
    await state.finish()

    # logging.info(f"{user.username} user was successfully created")
