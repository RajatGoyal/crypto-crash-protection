from strategy import *
from decimal import *


def trailing_stop_loss(exchange, pair, sell_amount, limit_percentage, id):
    left, right = pair.split('/')
    dollar_pair_symbol = '{}/USDT'.format(right)

    try:
        order_entry = Order.get(Order.provided_id == id)
        pair_ohlcs = exchange.ohlc(pair)
        dollar_pair_ohlcs = exchange.ohlc(dollar_pair_symbol)

        ath = order_entry.ath
        max_price = None

        for pair_ohlc in pair_ohlcs:
            if pair_ohlc[0] > order_entry.order_ts:
                for dollar_ohlc in dollar_pair_ohlcs:
                    if (pair_ohlc[0] == dollar_ohlc[0]) and (pair_ohlc[2] * dollar_ohlc[2] > order_entry.ath):
                        ath = pair_ohlc[2] * dollar_ohlc[2]
                        max_price = Decimal(pair_ohlc[2])

        print 'all time high is {}'.format(ath)

        if max_price:
            print 'updating your order to accomodate new ath'
            order_price = max_price - ((Decimal(limit_percentage) / 100) * max_price)
            order = update_order(order_entry, exchange, pair, sell_amount, order_price,
                                 order_price, "STOP_LOSS_LIMIT")
            update_order_entry(order, id, ath)
    except Order.DoesNotExist:
        dollar_pair_price = exchange.ticker(dollar_pair_symbol)
        pair_price = exchange.ticker(pair)

        order_price = pair_price - ((Decimal(limit_percentage)/100) * pair_price)
        ath = pair_price * dollar_pair_price

        order = create_order(exchange, pair, sell_amount, order_price, order_price, "STOP_LOSS_LIMIT")
        print('create order at {}'.format(order_price*dollar_pair_price))
        create_order_entry(order, pair, id, ath)