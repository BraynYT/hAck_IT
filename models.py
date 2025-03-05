from peewee import *
import datetime
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

class Topics(BaseModel):
    id = AutoField()
    title = CharField()
    category = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        db_table = "topics"

class Messages(BaseModel):
    topic = ForeignKeyField(Topics, backref='messages')
    author = CharField(default="Аноним")
    text = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        db_table = "messages"