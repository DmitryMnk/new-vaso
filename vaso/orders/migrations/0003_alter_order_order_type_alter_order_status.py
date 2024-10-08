# Generated by Django 5.1 on 2024-08-30 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_type",
            field=models.CharField(
                choices=[("SC", "Идеальный букет"), ("IB", "Витрина заказов")],
                max_length=100,
                verbose_name="Тип заказа",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Анкета заполнена", "Анкета заполнена"),
                    ("Букет собран", "Букет собран"),
                    ("Доработка букета", "Доработка букета"),
                    ("Ожидание оплаты", "Ожидание оплаты"),
                    ("Оплачено", "Оплачено"),
                    ("Поиск курьера", "Поиск курьера"),
                    ("Передано курьеру", "Передано курьеру"),
                    ("Доставлено", "Доставлено"),
                ],
                max_length=20,
                verbose_name="Статус",
            ),
        ),
    ]
