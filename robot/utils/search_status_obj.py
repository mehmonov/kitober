from robot.models import Status, TelegramUser, Book
from asgiref.sync import sync_to_async
@sync_to_async
def search_status_obj(query):
        status =  Status.objects.get(
            pk=query
        )
        return status
    