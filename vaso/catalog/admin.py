from django.contrib import admin
from .models import Bouquet, City, Package, Colors, BouquetPhotos


admin.site.register(City)
admin.site.register(Package)
admin.site.register(Colors)
admin.site.register(BouquetPhotos)


class BouquetPhotosInline(admin.TabularInline):
    model = BouquetPhotos
    extra = 1


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = (
        "id", 'name', "price", "discount", "is_sold", "created_at", "bouquet_type", "city", "package"
    )

    list_filter = ("is_sold", "bouquet_type", "city", "package")
    inlines = BouquetPhotosInline,
