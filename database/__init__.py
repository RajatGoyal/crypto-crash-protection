from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('orders.db')
db.connect()


class BaseModel(Model):
    class Meta:
        database = db
