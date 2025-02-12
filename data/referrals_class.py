import sqlalchemy
from .database import SqlAlchemyBase
from sqlalchemy.orm import relationship

class Referral(SqlAlchemyBase):
    __tablename__ = 'referrals'
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, autoincrement=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('users.telegram_id'))
    people_invited = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    people_bought_subscription = sqlalchemy.Column(sqlalchemy.Integer, default=0)
