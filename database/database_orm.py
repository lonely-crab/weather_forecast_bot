from peewee import *


db = SqliteDatabase('database/database.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    username = CharField()
    first_name = CharField()


def create_models():
    db.create_tables(BaseModel.__subclasses__())