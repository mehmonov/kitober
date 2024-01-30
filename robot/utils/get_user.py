from asgiref.sync import sync_to_async
from robot.models import TelegramUser


def get_user(chat_id):
    user= sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)
    return user
