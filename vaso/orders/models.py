from django.db import models

from orders.enums import Status
from user.models import UserProfile
from catalog.models import Bouquet, City
from django.utils import timezone


class Order(models.Model):
    amo_id = models.IntegerField(verbose_name='ID заказа на amo', null=True)
    order_type = models.CharField(max_length=100, null=False, verbose_name="Тип заказа")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Сумма")
    address = models.CharField(max_length=500, null=False, verbose_name="Адрес")
    city = models.ForeignKey(to=City, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Город")
    is_paid = models.BooleanField(default=False, null=False, verbose_name="Оплачено")
    status_history = models.JSONField(default=list, verbose_name="История статусов")
    expected_delivery_time = models.DateTimeField(verbose_name="Ожидаемое время доставки")
    # payment = models.ForeignKey(to=Payment, blank=True, on_delete=models.PROTECT, null=True,
    #                             verbose_name="Идентификатор платежа")
    courier = models.CharField(null=True, blank=True, verbose_name="Информация о курьере", max_length=255)
    profile = models.ForeignKey(to=UserProfile, on_delete=models.PROTECT, verbose_name="Пользователь")
    bouquet = models.ForeignKey(to=Bouquet, null=True, on_delete=models.PROTECT, verbose_name="Букет")

    class Meta:
        db_table = "orders"
        verbose_name = "Заказ"
        verbose_name_plural = 'Заказы'

    def set_status(self, status):
        if status != self.status:
            now = timezone.now().strftime('%d.%m.%Y %H:%M:%S %Z')
            self.status_history.append({"status": status, "at": now})
            self.save()

    @property
    def status(self):
        if self.status_history:
            status_value = self.status_history[-1].get("status") # noqa
            return Status(status_value)

    @property
    def amount(self):
        return round(self.price)  # noqa

    @property
    def total_with_discount(self):
        return round(self.amount - 0.1 * self.amount)  # noqa

    def __str__(self):
        return f'{self.id}'


class Payment(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Ожидает оплаты'),
        ('waiting_for_capture', 'Удержание средств'),
        ('succeeded', 'Оплачено'),
        ('canceled', 'Возврат удержанных средств'),
    )

    profile = models.ForeignKey(to=UserProfile, on_delete=models.PROTECT, verbose_name='Пользователь')
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Сумма")
    payment_id = models.UUIDField(verbose_name='Идентификатор платежа в платёжной системе')
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    method = models.CharField(max_length=40, null=True, verbose_name='Метод оплаты')
    system = models.CharField(max_length=20, default='yookassa', verbose_name='Платёжная система')
    url = models.URLField(verbose_name='Ссылка на оплату')
    created_at = models.DateTimeField(verbose_name='Дата создания')

    class Meta:
        db_table = "payments"
        verbose_name = "Платёж"
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return str(self.id)


    def __str__(self):
        return f'{self.id}'
