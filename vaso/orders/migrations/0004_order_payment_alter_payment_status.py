# Generated by Django 5.1 on 2024-08-31 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_alter_order_order_type_alter_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="orders.payment",
                verbose_name="Идентификатор платежа",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="status",
            field=models.CharField(
                choices=[
                    ("Ожидание оплаты", "Ожидает оплаты"),
                    ("Удержание средств", "Удержание средств"),
                    ("Оплачено", "Оплачено"),
                    ("Возврат удержанных средств", "Возврат удержанных средств"),
                ],
                default="pending",
                max_length=40,
                verbose_name="Статус",
            ),
        ),
    ]
