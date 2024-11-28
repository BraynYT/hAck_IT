from peewee import *
import os
from flask_login import UserMixin


current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(current_file)

db = SqliteDatabase(os.path.join(current_directory, 'DataBase.db'))

class BaseModel(Model):
    class Meta:
        database = db

class Users(UserMixin, BaseModel):
    username = CharField()
    password = IntegerField()
    email = CharField()
    created_on = CharField()
    roles = IntegerField()
    class Meta:
        db_table = 'users'
