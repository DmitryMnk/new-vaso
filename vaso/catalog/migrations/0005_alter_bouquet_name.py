# Generated by Django 5.1 on 2024-09-01 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_alter_bouquet_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bouquet",
            name="name",
            field=models.CharField(
                blank=True, max_length=80, null=True, verbose_name="Название"
            ),
        ),
    ]
