from strategy import *


def dollar_stop_loss(exchange, pair, sell_amount, sell_price, id):
    dollar_tickers = exchange.dollar_tickers()
    left, right = pair.split('/')
    dollar_pair = dollar_tickers.get('{}/USD'.format(right)) or dollar_tickers.get('{}/USDT'.format(right))
    price_secondary_pair = Decimal(sell_price) / Decimal(dollar_pair)

    try:
        order_entry = Order.get(Order.provided_id == id)
        print('Updating order')
        order = update_order(order_entry, exchange, pair, sell_amount, price_secondary_pair, price_secondary_pair,
                             "STOP_LOSS_LIMIT")
        update_order_entry(order, id)
    except Order.DoesNotExist:
        print('creating order')
        order = create_order(exchange, pair, sell_amount, price_secondary_pair, price_secondary_pair, "STOP_LOSS_LIMIT")
        create_order_entry(order, pair, id)