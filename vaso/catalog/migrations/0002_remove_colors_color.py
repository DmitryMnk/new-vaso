# Generated by Django 5.1 on 2024-08-25 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="colors",
            name="color",
        ),
    ]
