from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from django.conf import settings


bot = Bot(token='6428487731:AAH2RDsO-1HiwiS_eMhnhC0f4jANo6IWBaI', parse_mode=types.ParseMode.HTML, )
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage )
