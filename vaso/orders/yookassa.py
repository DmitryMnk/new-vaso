from uuid import UUID

from yookassa import Configuration, Payment
from yookassa.domain.common import ConfirmationType
from yookassa.domain.models import Currency
from yookassa.domain.request import PaymentRequestBuilder

from .enums import Status
from .models import Order
from .models import Payment as PaymentModel
from .const import YOOCASSA_SECRET_KEY, YOOCASSA_SHOP_ID
from vaso.settings import HOST

Configuration.account_id = YOOCASSA_SHOP_ID
Configuration.secret_key = YOOCASSA_SECRET_KEY


def create_payment(order: Order):

    order.set_status(Status.WAIT_PAYMENT)

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
            "return_url": f"{HOST}/orders"
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
        created_at=response.created_at
    )

    order.payment = payment
    order.save()

    return payment.url


def complete_payment(payment: PaymentModel):
    Payment.capture(str(payment.payment_id))


def canceled_payment(payment: PaymentModel):
    Payment.cancel(str(payment.payment_id))
