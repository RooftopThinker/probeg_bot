import sqlalchemy
from .database import SqlAlchemyBase


class Receipt(SqlAlchemyBase):
    __tablename__ = 'receipts'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('users.telegram_id'))
    link_valid_till = sqlalchemy.Column(sqlalchemy.DateTime)
    token = sqlalchemy.Column(sqlalchemy.String)
    is_money_transferred = sqlalchemy.Column(sqlalchemy.Boolean, default=False)