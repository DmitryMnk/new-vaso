# Generated by Django 5.1 on 2024-08-19 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_bouquetphotos_remove_bouquet_images_bouquet_photos"),
    ]

    operations = [
        migrations.AddField(
            model_name="bouquetphotos",
            name="bouqet",
            field=models.ForeignKey(
                default=1, on_delete=models.Model, to="catalog.bouquet"
            ),
            preserve_default=False,
        ),
    ]
