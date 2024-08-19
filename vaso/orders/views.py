import json
from ipaddress import ip_network, ip_address
from uuid import UUID

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from yookassa.domain.notification import WebhookNotification

from orders.utils import sync_order_status_by_payment
from vaso import settings

from orders.models import Payment


ALLOWED_IPS = [
    '185.71.76.0/27',
    '185.71.77.0/27',
    '77.75.153.0/25',
    '77.75.156.11',
    '77.75.156.35',
    '77.75.154.128/25',
    '2a02:5180::/32',
]

ALLOWED_NETWORKS = [ip_network(ip) for ip in ALLOWED_IPS]


def is_ip_allowed(ip: str) -> bool:
    ip_addr = ip_address(ip)
    return any(ip_addr in network for network in ALLOWED_NETWORKS)

@csrf_exempt
def webhook_payment(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        client_ip = request.META.get('REMOTE_ADDR')

        if not settings.DEBUG and (not client_ip or not is_ip_allowed(client_ip)):
            return HttpResponseForbidden("Forbidden")

        data = json.loads(request.body)
        webhook_notification = WebhookNotification(data)

        payment_event = webhook_notification.object
        payment: Payment = Payment.objects.get(payment_id=UUID(payment_event.id))
        payment.method = payment_event.payment_method.type
        payment.status = payment_event.status
        payment.save()
        sync_order_status_by_payment(payment)

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)
