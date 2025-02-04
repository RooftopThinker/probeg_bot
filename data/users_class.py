import sqlalchemy
from .database import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True, nullable=False)
    telegram_username = sqlalchemy.Column(sqlalchemy.String)
    telegram_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    phone_number = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String)
    role = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    full_name = sqlalchemy.Column(sqlalchemy.String)
    company_name = sqlalchemy.Column(sqlalchemy.String)
    position = sqlalchemy.Column(sqlalchemy.String)
    is_accepted = sqlalchemy.Column(sqlalchemy.Boolean)
    subscription_till = sqlalchemy.Column(sqlalchemy.DATE)
