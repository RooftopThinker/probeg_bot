import sqlalchemy
from .database import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True, nullable=False)
    telegram_username = sqlalchemy.Column(sqlalchemy.String)
    telegram_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    phone_number = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    full_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    company_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    position = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_accepted = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    subscription_till = sqlalchemy.Column(sqlalchemy.DATE)
