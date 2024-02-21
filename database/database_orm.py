from peewee import *


db = SqliteDatabase("database/database.db")


class BaseModel(Model):
    """
    Base model class for all models.
    """

    class Meta:
        database = db


class User(BaseModel):
    """
    User model class.
    """

    user_id = IntegerField(primary_key=True)
    username = CharField()
    first_name = CharField()


def create_models():
    db.create_tables(BaseModel.__subclasses__())
