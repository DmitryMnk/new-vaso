import json
import logging
from datetime import datetime
from ipaddress import ip_network, ip_address
from uuid import UUID

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from orders.utils import sync_order_status_by_payment, set_amo_status
from vaso import settings
logger = logging.getLogger()
logging.basicConfig(filename='logs.log', level=logging.INFO)
from orders.models import Payment, Order

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
    logger.info(f'{request.method}')
    if request.method == 'POST':
        client_ip = request.META.get('REMOTE_ADDR')

        if not settings.DEBUG and (not client_ip or not is_ip_allowed(client_ip)):
            return HttpResponseForbidden("Forbidden")
        data = json.loads(request.body)
        logger.info(f'{data}')
        payment_id = data.get('object').get('id')
        event = data.get('object').get('status')


        payment: Payment = Payment.objects.get(payment_id=UUID(payment_id))
        sync_order_status_by_payment(payment, event)

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)


class CreateBouquetOrder(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        if not request.user.is_authenticated:
            return Response(status=403)


@csrf_exempt
def amo_webhook(request: WSGIRequest) -> JsonResponse:
    logger.info(request)

    if request.method == 'POST':
        try:
            if not request.body:
                return JsonResponse({'error': 'Empty request body'}, status=400)

            data = request.POST
            logger.info(f'{datetime.now()!r}{data}')
            deal_id = int(data.get('leads[status][0][id]'))
            deal_stage_id = int(data.get('leads[status][0][status_id]'))
            logger.info(f'{deal_id=}{deal_stage_id=}')
            order = Order.objects.get(amo_id=deal_id)
            set_amo_status(order, deal_stage_id)
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)


    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


