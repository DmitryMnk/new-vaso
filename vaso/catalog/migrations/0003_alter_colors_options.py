# Generated by Django 5.1 on 2024-08-18 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_colors_alter_package_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="colors",
            options={"verbose_name": "Цвет", "verbose_name_plural": "Цвета"},
        ),
    ]
