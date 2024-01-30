from django.contrib import admin

from .models import Status, TelegramUser, Book


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = [ 'full_name', 'chat_id',  'id']


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(Book)
admin.site.register(Status)
