from django.urls import path
from .views import BouquetDetail, CreateBouquetView

urlpatterns = [
    path('bouquet/<int:pk>', BouquetDetail.as_view(), name='bouquet_detail'),
    path('create_bouquet/', CreateBouquetView.as_view(), name='create_bouquet')
]
