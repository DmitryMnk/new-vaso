# Generated by Django 5.1 on 2024-08-18 08:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("catalog", "0003_alter_colors_options"),
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amo_id",
                    models.IntegerField(null=True, verbose_name="ID заказа на amo"),
                ),
                (
                    "order_type",
                    models.CharField(max_length=100, verbose_name="Тип заказа"),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=7, verbose_name="Сумма"
                    ),
                ),
                ("address", models.CharField(max_length=500, verbose_name="Адрес")),
                (
                    "is_paid",
                    models.BooleanField(default=False, verbose_name="Оплачено"),
                ),
                (
                    "status_history",
                    models.JSONField(default=list, verbose_name="История статусов"),
                ),
                (
                    "expected_delivery_time",
                    models.DateTimeField(verbose_name="Ожидаемое время доставки"),
                ),
                (
                    "courier",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Информация о курьере",
                    ),
                ),
                (
                    "bouquet",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="catalog.bouquet",
                        verbose_name="Букет",
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.city",
                        verbose_name="Город",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="user.userprofile",
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заказ",
                "verbose_name_plural": "Заказы",
                "db_table": "orders",
            },
        ),
    ]
