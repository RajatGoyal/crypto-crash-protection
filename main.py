# coding=utf-8
import yaml
import time
import sqlite3

from exchanges.binance import Binance
from notifications.pushbullet import send_notification
from strategy.dollar_stop_loss import dollar_stop_loss
from strategy.trailing_stop_loss import trailing_stop_loss
from database.orders import Order
from database import *


with open("orders.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

pushbullet_token = cfg['PUSHBULLET']
send_notification(pushbullet_token, 'crash-protection-script', 'started')

exchange = Binance(cfg['API_KEY'], cfg['API_SECRET'])

while True:
    for order in cfg['ORDERS']:
        if not order['id']:
            raise Exception, 'id should be present to place a order'

        if order['order_type'] == 'dollar-stop-loss':
            #dollar_stop_loss(exchange, order['pair'], order['sell_amount'], order['sell_price'], order['id'])
            pass
        if order['order_type'] == 'trailing-stop-loss':
            trailing_stop_loss(exchange, order['pair'], order['sell_amount'], order['limit_percentage'], order['id'])

    time.sleep(10)