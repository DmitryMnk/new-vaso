from django.urls import path
from .views import MainView, download_file, DPInfoView, AboutView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('about/', AboutView.as_view(), name='about'),
    path('policy/', download_file, name='policy'),
    path('dp_info', DPInfoView.as_view(), name='delivery_and_payment_info'),
]
