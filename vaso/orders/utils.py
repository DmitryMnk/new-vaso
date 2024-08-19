from catalog.models import Bouquet
from .enums import Status, OrderType
from .models import Order
from .models import Payment
from . import yookassa


CANCELLABLE_STATUSES = (
    Status.NEW,
    Status.ORDER_PREPARE,
    Status.ORDER_PLACED,
    Status.WAIT_PAYMENT,
    Status.PAY_HELD,
    Status.COURIER_LOOKUP,
    Status.COURIER_FOUND,
)


def release_bouquet(bouquet_id):
    bouquet: Bouquet = Bouquet.objects.get(pk=bouquet_id)
    bouquet.is_reserved = False

    if bouquet.bouquet_type == 'IB':
        bouquet.bouquet_type = 'SC'

    bouquet.save()


def sync_order_status_by_payment(payment: Payment):

    order: Order = Order.objects.get(payment=payment)

    match payment.status:
        case 'pending':
            order.set_status(Status.WAIT_PAYMENT)
        case 'waiting_for_capture':

            order.set_status(Status.PAY_HELD)
            order.set_status(Status.COURIER_LOOKUP)
        case 'succeeded':
            order.bouquet.is_sold = True
            order.is_paid = True
            order.set_status(Status.PAY_COMPLETE)
        case 'canceled':
            order.set_status(Status.CANCEL)


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
