from django.urls import path
from .views import MainView
from orders.views import webhook_payment

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('webhook/payment/', webhook_payment, name='webhook_payment')
]
