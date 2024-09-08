from django.db import models

from orders.enums import Status
from user.models import UserProfile
from catalog.models import Bouquet, City
from django.utils import timezone


class Order(models.Model):

    SC = 'SC'
    IB = 'IB'
    QUEST_COMPLETE = 'Анкета заполнена'
    BOUQUET_COMPLETE = 'Букет собран'
    BOUQUET_UPDATING = 'Доработка букета'
    WAIT_PAYMENT = 'Ожидание оплаты'
    PAYMENT_COMPLETE = 'Оплачено'
    COURIER_LOOKUP = 'Поиск курьера'
    TRANSFER = 'Передано курьеру'
    COMPLETE = 'Доставлено'

    ORDERS_CHOICES = (
        (SC, 'Идеальный букет'),
        (IB, 'Витрина заказов')
    )

    STATUS_CHOICES = (

        (QUEST_COMPLETE ,'Анкета заполнена'),
        (BOUQUET_COMPLETE ,'Букет собран'),
        (BOUQUET_UPDATING, 'Доработка букета'),
        (WAIT_PAYMENT ,'Ожидание оплаты'),
        (PAYMENT_COMPLETE ,'Оплачено'),
        (COURIER_LOOKUP ,'Поиск курьера'),
        (TRANSFER, 'Передано курьеру'),
        (COMPLETE, 'Доставлено'),
    )

    amo_id = models.IntegerField(verbose_name='ID заказа на amo', null=True)
    order_type = models.CharField(max_length=100, choices=ORDERS_CHOICES, verbose_name="Тип заказа")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Сумма")
    address = models.CharField(max_length=500, null=False, verbose_name="Адрес")
    city = models.ForeignKey(to=City, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Город")
    is_paid = models.BooleanField(default=False, null=False, verbose_name="Оплачено")
    status = models.CharField(max_length=20, verbose_name='Статус', choices=STATUS_CHOICES)
    status_history = models.JSONField(default=list, verbose_name="История статусов")
    expected_delivery_time = models.DateTimeField(verbose_name="Ожидаемое время доставки")
    payment = models.ForeignKey(to='Payment', blank=True, on_delete=models.PROTECT, null=True,
                                 verbose_name="Идентификатор платежа")
    courier = models.CharField(null=True, blank=True, verbose_name="Информация о курьере", max_length=255)
    profile = models.ForeignKey(to=UserProfile, on_delete=models.PROTECT, verbose_name="Пользователь")
    bouquet = models.ForeignKey(to=Bouquet, null=True, on_delete=models.PROTECT, verbose_name="Букет")

    def set_status(self, status):
        now = timezone.now().strftime('%d.%m.%Y %H:%M:%S %Z')
        self.status_history.append({"status": status, "at": now}) # noqa
        self.save()


    class Meta:
        db_table = "orders"
        verbose_name = "Заказ"
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.id} {self.order_type}'


class Payment(models.Model):
    PENDING = 'Ожидание оплаты'
    WAITING_FOR_CAPTURE = 'Удержание средств'
    SUCCEEDED = 'Оплачено'
    CANCELED = 'Возврат удержанных средств'


    STATUS_CHOICES = (
        (PENDING, 'Ожидает оплаты'),
        (WAITING_FOR_CAPTURE, 'Удержание средств'),
        (SUCCEEDED, 'Оплачено'),
        (CANCELED, 'Возврат удержанных средств'),
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
