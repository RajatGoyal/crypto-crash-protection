from database.orders import Order
from decimal import *
from peewee import *
from database.orders import *
import datetime


def utc_timestamp():
    d = datetime.datetime.utcnow()
    epoch = datetime.datetime(1970, 1, 1)
    t = (d - epoch).total_seconds() * 1000
    return int(t)


def create_order(exchange, pair, sell_amount, price, stop_price, stop_loss_type):
    return exchange.sell_limit(pair, sell_amount, price,  {"type": stop_loss_type, "stopPrice": stop_price})


def update_order(order_entry, exchange, pair, sell_amount, price, stop_price, stop_loss_type):
    order = exchange.fetch_order(order_entry.exchange_id, pair)
    exchange.cancel_order(order_entry.exchange_id, pair)
    executed_qty = Decimal(order['info']['executedQty'])
    sell_amount -= executed_qty

    if executed_qty > 0:
        send_notification(pushbullet_token, 'Order Executed {} {}'.format(pair, executed_qty), '')

    return create_order(exchange, pair, sell_amount, price, stop_price, stop_loss_type)


def create_order_entry(order, pair, id, ath=None):
    Order.create(provided_id=id, order_type=order['type'], exchange_id=order['orderId'], active=True,
                 pair=pair, order_ts=utc_timestamp(), ath=ath)


def update_order_entry(order, id, ath=None):
    try:
        order_entry = Order.get(Order.provided_id == id)
        order_entry.exchange_id = order['orderId']
        order_entry.order_ts = utc_timestamp()
        order_entry.ath = ath
        order_entry.save()
    except Order.DoesNotExist:
        pass
