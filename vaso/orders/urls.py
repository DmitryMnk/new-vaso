from django.urls import path

from .views import amo_webhook, webhook_payment

urlpatterns = [
    path('webhook/amo_deals', amo_webhook, name='amo'),
    path('webhook/yookassa', webhook_payment, name='yookassa'),
]
