from django.db import models
from datetime import datetime, timedelta
EXCHANGE_STATUS_CHOICES = [
    ('requested', "So'ralgan"),
    ('accepted', "Qabul qilingan"),
    ('rejected', "Rad etilgan"),
    ('completed', "Tugallangan"),
]
PROVISION_CHOICES = [
    ('self', "O'zim yetkazaman"),
    ('post', "Pochtadan yuboraman"),
    ('pickup', "O'zingiz kelib olib ketasiz"),
]
RETURNED_DATE = [
    (5, 5),
    (10, 10),
    (15, 15),
    (20, 20)
]
class TelegramUser(models.Model):
    full_name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    username = models.CharField(
        max_length=60
    )
    chat_id = models.BigIntegerField()
    phone_number = models.CharField(
        max_length=30
    )
    location = models.CharField(
        max_length=200
    )
    def __str__(self):
        return str(self.chat_id)


    def get_user(self):
        return self.full_name

    # def set_user(self, chat_id):
    #     self.chat_id= chat_id

        
class Book(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kitob nomi")
    author = models.CharField(max_length=255, verbose_name="Kitob muallifi")
    genre = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    owner = models.ForeignKey(TelegramUser,  on_delete=models.CASCADE, verbose_name="Kitobning egasi", related_name="userbooks")
    image = models.CharField(max_length=255, verbose_name="Kitob rasmi")

    def __str__(self) -> str:
        return self.name

from django.utils import timezone

class Status(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Almashilgan kitob")
    status = models.CharField(max_length=10, choices=EXCHANGE_STATUS_CHOICES, verbose_name="Almashuv statusi", default='requested' )
    borrower = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, verbose_name="Kitobni olgan foydalanuvchi")
    borrowed_date = models.DateTimeField(auto_now_add=True, verbose_name="Kitobni olgan sana")
    return_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=10), editable=False, verbose_name="Kitobni qaytarish muddati")
    provision = models.CharField(max_length=6, choices=PROVISION_CHOICES, default=None) 
    @property
    def owner_username(self):
        return self.book.owner.pk if self.book and self.book.owner else None

    def __str__(self) -> str:
        return self.book.name
