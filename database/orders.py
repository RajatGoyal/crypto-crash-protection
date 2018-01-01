from database import *
from peewee import *


class Order(BaseModel):
    order_type = CharField()
    provided_id = IntegerField()
    exchange_id = IntegerField()
    active = BooleanField()
    pair = CharField()
    ath = DecimalField()
    order_ts = IntegerField()

try:
    db.create_tables([Order])
except:
    pass