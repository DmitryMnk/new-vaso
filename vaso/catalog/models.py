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

    SC = 'SC'
    IB = 'IB'

    CHOICES = (
        ("SC", "Онлайн-витрина"),
        ("IB", "Идеальный букет"),
    )

    name = models.CharField(max_length=80, null=True, blank=True, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')
    discount = models.DecimalField(default=0.0, max_digits=7, decimal_places=2, verbose_name="Скидка")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    is_reserved = models.BooleanField(verbose_name="Зарезервировано", default=False)
    is_sold = models.BooleanField(verbose_name="Продано", default=False)
    created_at = models.TimeField(auto_now=True, verbose_name="Создано")
    bouquet_type = models.CharField(max_length=100, verbose_name="Тип букета", choices=CHOICES)
    city = models.ForeignKey(to='City', on_delete=models.PROTECT, null=True, verbose_name="Город")
    package = models.ForeignKey(to='Package', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Упаковка")

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

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"

    def __str__(self):
        return self.name

class BouquetPhotos(models.Model):
    image = models.ImageField(verbose_name='Фото букета', upload_to='bouqets/photos')
    bouquet = models.ForeignKey(Bouquet, on_delete=models.PROTECT, related_name='photos')

    class Meta:
        verbose_name = "Фото букета"
        verbose_name_plural = "Фото букетов"
