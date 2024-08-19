# Generated by Django 5.1 on 2024-08-18 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=7, verbose_name="Сумма"
                    ),
                ),
                (
                    "payment_id",
                    models.UUIDField(
                        verbose_name="Идентификатор платежа в платёжной системе"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Ожидает оплаты"),
                            ("waiting_for_capture", "Удержание средств"),
                            ("succeeded", "Оплачено"),
                            ("canceled", "Возврат удержанных средств"),
                        ],
                        default="pending",
                        max_length=40,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "method",
                    models.CharField(
                        max_length=40, null=True, verbose_name="Метод оплаты"
                    ),
                ),
                (
                    "system",
                    models.CharField(
                        default="yookassa",
                        max_length=20,
                        verbose_name="Платёжная система",
                    ),
                ),
                ("url", models.URLField(verbose_name="Ссылка на оплату")),
                ("created_at", models.DateTimeField(verbose_name="Дата создания")),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="user.userprofile",
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Платёж",
                "verbose_name_plural": "Платежи",
                "db_table": "payments",
            },
        ),
    ]
