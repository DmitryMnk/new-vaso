from enum import Enum


class Status(str, Enum):
    NEW = 'Новый'
    WAIT_PAYMENT = 'Ожидает оплаты'
    PAY_HELD = 'Удержание средств'
    ORDER_PREPARE = 'Заказ собирается'
    ORDER_PLACED = 'Заказ собран'
    COURIER_LOOKUP = 'Поиск курьера'
    COURIER_FOUND = 'Курьер найден'
    PAY_COMPLETE = 'Заказ оплачен'
    REFUND_OF_PAYMENT = 'Возврат платежа'
    WAIT_CANCELED = 'Ожидает отмены'
    CANCEL = 'Заказ отменён'
    DELIVERY = 'Заказ в доставке'
    DELIVERED = 'Заказ доставлен'


class OrderType(str, Enum):
    IB = 'IB'
    SC = 'SC'
