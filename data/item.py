import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Item(SqlAlchemyBase):
    __tablename__ = 'item'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    condition = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    photos = sqlalchemy.Column(sqlalchemy.BLOB, nullable=False)  # доработать
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("user.id"),
                                default='me')
    user = orm.relationship('User')

    def __repr__(self):
        return f'{self.category} {self.title} {self.condition} ' \
               f'{self.description} {self.price}'
