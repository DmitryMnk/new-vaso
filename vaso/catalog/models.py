from django.db import models


class City(models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name='Название')

    class Meta:
        db_table = "cities"
        verbose_name = "Город"
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class Package(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    image = models.ImageField(upload_to='packages', verbose_name='Изображение упаковки')

    class Meta:
        db_table = "packages"
        verbose_name = "Упаковку"
        verbose_name_plural = 'Упаковки'

    def __str__(self):
        return self.name


class Bouquet(models.Model):
    choices = (
        ("SC", "Онлайн-витрина"),
        ("IB", "Идеальный букет"),
    )

    name = models.CharField(max_length=80, unique=True, null=True, verbose_name='Название')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.0, max_digits=7, decimal_places=2, verbose_name="Скидка")
    description = models.TextField(verbose_name="Описание")
    is_reserved = models.BooleanField(null=False, verbose_name="Зарезервировано")
    is_sold = models.BooleanField(null=False, verbose_name="Продано")
    created_at = models.TimeField(auto_now=True, verbose_name="Создано")
    bouquet_type = models.CharField(max_length=100, verbose_name="Тип букета", choices=choices)
    city = models.ForeignKey(to='City', on_delete=models.PROTECT, null=True, verbose_name="Город")
    package = models.ForeignKey(to='Package', on_delete=models.PROTECT, null=False, verbose_name="Упаковка")

    class Meta:
        db_table = "bouquets"
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"

    @property
    def amount(self):
        return round(self.price)

    def __str__(self):
        return f'{self.id}'


class Colors(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    color = models.CharField(max_length=7, unique=True, verbose_name='HEX код')

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"


class BouquetPhotos(models.Model):
    image = models.ImageField(verbose_name='Фото букета', upload_to='bouqets/photos')
    bouquet = models.ForeignKey(Bouquet, on_delete=models.PROTECT, related_name='photos')

    class Meta:
        verbose_name = "Фото букета"
        verbose_name_plural = "Фото букетов"
