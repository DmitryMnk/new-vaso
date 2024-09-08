from datetime import timedelta
from typing import Dict
from uuid import UUID

from django.conf import settings
from yookassa.domain.common import ConfirmationType
from yookassa.domain.models import Currency
from yookassa.domain.request import PaymentRequestBuilder
from yookassa import Payment

from catalog.models import Bouquet
from catalog.utils import create_bouquet
from main.amocrm import create_deal_showcase, create_deal_ib, PIPELINE, update_deal_status
from .enums import Status, OrderType
from .models import Order
from .models import Payment as PaymentModel
from . import yookassa
from django.utils import timezone
from main.amocrm import PIPELINE
CANCELLABLE_STATUSES = (
    Status.NEW,
    Status.ORDER_PREPARE,
    Status.ORDER_PLACED,
    Status.WAIT_PAYMENT,
    Status.PAY_HELD,
    Status.COURIER_LOOKUP,
    Status.COURIER_FOUND,
)

ORDER_STATUS = {
    68497894: Order.QUEST_COMPLETE,
    68706382: Order.BOUQUET_COMPLETE,
    68706386: Order.BOUQUET_UPDATING,
    68706390: Order.WAIT_PAYMENT,
    68706394: Order.PAYMENT_COMPLETE,
    68706398: Order.COURIER_LOOKUP,
    68706402: Order.TRANSFER,
    68706406: Order.COMPLETE
}


def release_bouquet(bouquet_id):
    bouquet: Bouquet = Bouquet.objects.get(pk=bouquet_id)
    bouquet.is_reserved = False

    if bouquet.bouquet_type == 'IB':
        bouquet.bouquet_type = 'SC'

    bouquet.save()


def get_available_statuses(current_status: Status, order_type: OrderType):
    status_flow = {
        Status.WAIT_PAYMENT: [Status.CANCEL],
        Status.PAY_HELD: [Status.CANCEL],
        Status.COURIER_LOOKUP: [Status.COURIER_FOUND, Status.CANCEL],
        Status.COURIER_FOUND: [Status.CANCEL],
        Status.PAY_COMPLETE: [Status.DELIVERY],
        Status.DELIVERY: [Status.DELIVERED],
    }

    if order_type == OrderType.IB:
        status_flow_ib = {
            Status.NEW: [Status.ORDER_PREPARE, Status.CANCEL],
            Status.ORDER_PREPARE: [Status.ORDER_PLACED, Status.CANCEL],
            Status.ORDER_PLACED: [Status.CANCEL]
        }

        status_flow.update(status_flow_ib)

    return status_flow.get(current_status, [])


def update_order_status(order: Order, status: Status):

    match status, order.order_type, order.status:
        case Status.ORDER_PREPARE, OrderType.IB, _:
            order.set_status(status)

        case Status.ORDER_PLACED, OrderType.IB, _:
            order.set_status(status)
            yookassa.create_payment(order)

        case Status.COURIER_FOUND, _, _:
            order.set_status(status)
            yookassa.complete_payment(order.payment)

        case Status.DELIVERY, _, _:
            order.set_status(status)

        case Status.DELIVERED, _, _:
            order.set_status(status)

        case Status.CANCEL, OrderType.IB, Status.NEW | Status.ORDER_PREPARE:
            order.set_status(status)

        case Status.CANCEL, OrderType.IB, Status.ORDER_PLACED:
            release_bouquet(order.bouquet_id)
            order.set_status(status)

        case Status.CANCEL, _, Status.WAIT_PAYMENT:
            release_bouquet(order.bouquet_id)
            order.set_status(Status.WAIT_CANCELED)

        case Status.CANCEL, _, _ if order.status not in (Status.PAY_COMPLETE, Status.DELIVERY, Status.DELIVERED):
            release_bouquet(order.bouquet_id)
            order.set_status(Status.WAIT_CANCELED)
            yookassa.canceled_payment(order.payment)


def set_amo_status(order: Order, status_id):
    status = ORDER_STATUS[status_id]
    order.status = status
    order.set_status(ORDER_STATUS)
    order.save()


def create_order(is_fast: bool, order_data: Dict) -> Order:
    new_order = Order.objects.create(
        price=order_data.get('price'),
        address=order_data.get('address'),
        city=order_data.get('city'),
        profile=order_data.get('profile'),
        expected_delivery_time=timezone.now() + timedelta(hours=2),
        bouquet=order_data.get('bouquet'),

    )

    deal_data = {
        'address': order_data.get('address'),
        'order_type': order_data.get('bouquet').bouquet_type,
        'order_id': new_order.id,
        'date': new_order.expected_delivery_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'contact_id': order_data.get('profile').amo_id,
        'price': order_data.get('price')
    }

    if not is_fast:
        deal_data.update({
            'colors': ', '.join(order_data.get('colors')),
            'package': order_data.get('package'),
            'else': order_data.get('else'),
        })
        amo_id = create_deal_ib(deal_data)['_embedded']['leads'][0]['id']
        new_order.order_type = Order.IB
        new_order.amo_id = amo_id
        new_order.save()

    else:
        amo_id = create_deal_showcase(deal_data)['_embedded']['leads'][0]['id']
        new_order.order_type = Order.SC
        new_order.amo_id = amo_id
        new_order.save()

    return new_order


def create_payment(order):
    builder = PaymentRequestBuilder()
    builder.set_amount(
        {
            "value": order.price,
            "currency": Currency.RUB
        }
    )

    builder.set_confirmation(
        {
            "type": ConfirmationType.REDIRECT,
            "return_url": f"{settings.HOST}/orders"
        }

    )

    builder.set_capture(False)
    builder.set_description(f"Заказ №{str(order.id)}")
    builder.set_metadata(
        {"orderNumber": str(order.id)}
    )

    request = builder.build()

    response = Payment.create(request)

    payment: PaymentModel = PaymentModel.objects.create(
        profile=order.profile,
        amount=response.amount.value,
        payment_id=UUID(response.id),
        url=response.confirmation.confirmation_url,
        created_at=response.created_at,
        status=PaymentModel.PENDING,
    )

    order.payment = payment
    order.save()

    return payment.url


def sync_order_status_by_payment(payment: PaymentModel, event: str):
    order: Order = Order.objects.get(payment=payment)
    amo_id = order.amo_id
    statuses = {
        'waiting_for_capture': PIPELINE['statuses']['Оплачивают заказ'],
        'succeeded': PIPELINE['statuses']['Оплачено'],
    }

    match event:
        case 'waiting_for_capture':
            update_deal_status(
                {
                    'deal_id': amo_id,
                    'pipeline_id': PIPELINE['id'],
                    'status_id': statuses['waiting_for_capture']
                }
            )
            order.status = Order.QUEST_COMPLETE
            order.set_status(Order.QUEST_COMPLETE)
            order.save()


        case 'succeeded':
            update_deal_status(
                {
                    'deal_id': amo_id,
                    'pipeline_id': PIPELINE['id'],
                    'status_id': statuses['succeeded']
                }
            )
            payment.status = PaymentModel.SUCCEEDED
            payment.save()
            order.bouquet.is_sold = True
            order.is_paid = True
            order.status = order.PAYMENT_COMPLETE
            order.set_status(Order.PAYMENT_COMPLETE)
            order.save()

