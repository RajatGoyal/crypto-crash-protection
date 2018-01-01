import ccxt
from ccxt.base.errors import InvalidOrder
from decimal import *


class Exchange:
    def tickers(self):
        return self.exchange.fetch_tickers()

    def ticker(self, market):
        ticker = self.exchange.fetch_ticker(market)['info']['lastPrice']
        return Decimal(ticker)

    def dollar_tickers(self):
        raise NotImplementedError

    def balances(self):
        formatted_balances = []
        balances = self.exchange.fetch_balance()

        for key, value in balances.iteritems():
            if key in ['free', 'total', 'used', 'info']:
                continue
            balance_total = float(value['total'])
            arr_row = {'currency': key, 'balance': float(balance_total), 'available': float(value['free'])}
            formatted_balances.append(arr_row)

        return formatted_balances

    def get_balance(self, currency):
        return filter(lambda x: x['currency'] == currency, self.balances())[0]

    def ohlc(self, market, timeframe='1m'):
        return self.exchange.fetch_ohlcv(market, timeframe)

    def open_orders(self, market):
        return self.exchange.open_orders(market)

    def fetch_order(self, order_id, symbol=None):
        return self.exchange.fetch_order(order_id, symbol)

    def cancel_order(self, order_id, symbol=None):
        return self.exchange.cancel_order(order_id, symbol)

    def sell_limit(self, market, sell_amount, sell_price, params={}):
        try:
            result = self.exchange.createLimitSellOrder(market, float(sell_amount), float(sell_price), params)
            return_result = result['info']
            return_result['uuid'] = return_result['orderId']  # for consistency in the main code
            return return_result
        except InvalidOrder:
            print 'MIN_TRADE_REQUIREMENT_NOT_MET for {}'.format(market)

    def fetch_trades(self, symbol):
        return self.exchange.fetch_trades(symbol)