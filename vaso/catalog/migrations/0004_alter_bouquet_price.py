# Generated by Django 5.1 on 2024-09-01 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_alter_bouquet_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bouquet",
            name="price",
            field=models.IntegerField(verbose_name="Цена"),
        ),
    ]
