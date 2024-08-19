# Generated by Django 5.1 on 2024-08-19 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_bouquetphotos_bouqet"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bouquet",
            name="photos",
        ),
        migrations.RemoveField(
            model_name="bouquetphotos",
            name="bouqet",
        ),
        migrations.AddField(
            model_name="bouquetphotos",
            name="bouquet",
            field=models.ForeignKey(
                default=1,
                on_delete=models.Model,
                related_name="photos",
                to="catalog.bouquet",
            ),
            preserve_default=False,
        ),
    ]
