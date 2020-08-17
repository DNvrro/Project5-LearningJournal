import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from peewee import *

DB = SqliteDatabase('journal.db')


class Entry(Model):
    title = CharField()
    date = DateField()
    time_spent = IntegerField()
    what_i_learned = TextField()
    resources_to_remember = TextField()

    class Meta:
        database = DB
        ordering = ('-date',)

    
    @classmethod
    def create_entry(cls, title, date, time_spent, what_i_learned, resources_to_remember):
        try:
            with DB.transaction():
                cls.create(
                    title=title,
                    date=date,
                    time_spent=time_spent,
                    what_i_learned=what_i_learned,
                    resources_to_remember=resources_to_remember
                )
        except IntegrityError:
            raise ValueError('This entry already exists')





class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=30)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DB

    
    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            with DB.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin
                )
        except IntegrityError:
            raise ValueError("User already exists")


def initialize():
    DB.connect()
    DB.create_tables([Entry, User], safe=True)
    DB.close()