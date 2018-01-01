from exchanges import Exchange
from decimal import Decimal, getcontext
import ccxt

getcontext().prec = 6


class Binance(Exchange):
    def __init__(self, api_key, api_secret):
        self.exchange = getattr(ccxt, 'binance')({
            'apiKey': api_key,
            'secret': api_secret,
        })

    def dollar_tickers(self):
        result = {}
        tickers = self.tickers()
        for key, value in tickers.iteritems():
            if '/USDT' in key:
                result[key] = value['ask']
            else:
                left, right = key.split('/')
                dollar_pair = tickers.get('{}/USDT'.format(right), {}).get('ask')
                if dollar_pair:
                    result[key] = value['ask'] * dollar_pair

        return result