import sqlalchemy
from .database import SqlAlchemyBase


class Receipt(SqlAlchemyBase):
    __tablename__ = 'receipts'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    order_id = sqlalchemy.Column(sqlalchemy.String, unique=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('users.telegram_id'))
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    is_paid = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
