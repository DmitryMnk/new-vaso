from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь')
    points = models.IntegerField(verbose_name='Баллы', default=0)
    phone_number = PhoneNumberField(unique=True)
    amo_id = models.IntegerField(verbose_name='ID контакта amo', unique=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone_number'

    class Meta:
        db_table = "profiles"
        verbose_name = "Профиль пользователя"
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'{self.user.first_name} {self.phone_number}'

