# Generated by Django 5.1 on 2024-08-18 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_payment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment",
            name="amount",
        ),
        migrations.RemoveField(
            model_name="payment",
            name="status",
        ),
    ]
