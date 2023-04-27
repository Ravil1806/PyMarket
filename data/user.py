import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    address = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    confirmed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    phone_number = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    items = orm.relationship("Item", back_populates='user')

    def __repr__(self):
        return f'{self.email} {self.name} {self.surname} {self.hashed_password}'
