# Generated by Django 5.1 on 2024-08-25 07:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Bouquet",
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
                    "name",
                    models.CharField(max_length=80, null=True, verbose_name="Название"),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=7, verbose_name="Цена"
                    ),
                ),
                (
                    "discount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=7,
                        verbose_name="Скидка",
                    ),
                ),
                ("description", models.TextField(null=True, verbose_name="Описание")),
                (
                    "is_reserved",
                    models.BooleanField(default=False, verbose_name="Зарезервировано"),
                ),
                ("is_sold", models.BooleanField(default=False, verbose_name="Продано")),
                ("created_at", models.TimeField(auto_now=True, verbose_name="Создано")),
                (
                    "bouquet_type",
                    models.CharField(
                        choices=[("SC", "Онлайн-витрина"), ("IB", "Идеальный букет")],
                        max_length=100,
                        verbose_name="Тип букета",
                    ),
                ),
            ],
            options={
                "verbose_name": "Букет",
                "verbose_name_plural": "Букеты",
                "db_table": "bouquets",
            },
        ),
        migrations.CreateModel(
            name="City",
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
                    "name",
                    models.CharField(
                        max_length=80, unique=True, verbose_name="Название"
                    ),
                ),
            ],
            options={
                "verbose_name": "Город",
                "verbose_name_plural": "Города",
                "db_table": "cities",
            },
        ),
        migrations.CreateModel(
            name="Colors",
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
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Название"
                    ),
                ),
                (
                    "color",
                    models.CharField(max_length=7, unique=True, verbose_name="HEX код"),
                ),
            ],
            options={
                "verbose_name": "Цвет",
                "verbose_name_plural": "Цвета",
            },
        ),
        migrations.CreateModel(
            name="Package",
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
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Название"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="packages", verbose_name="Изображение упаковки"
                    ),
                ),
            ],
            options={
                "verbose_name": "Упаковку",
                "verbose_name_plural": "Упаковки",
                "db_table": "packages",
            },
        ),
        migrations.CreateModel(
            name="BouquetPhotos",
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
                    "image",
                    models.ImageField(
                        upload_to="bouqets/photos", verbose_name="Фото букета"
                    ),
                ),
                (
                    "bouquet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="photos",
                        to="catalog.bouquet",
                    ),
                ),
            ],
            options={
                "verbose_name": "Фото букета",
                "verbose_name_plural": "Фото букетов",
            },
        ),
        migrations.AddField(
            model_name="bouquet",
            name="city",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="catalog.city",
                verbose_name="Город",
            ),
        ),
        migrations.AddField(
            model_name="bouquet",
            name="package",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="catalog.package",
                verbose_name="Упаковка",
            ),
        ),
    ]
