import sqlalchemy
from .database import SqlAlchemyBase


class Application(SqlAlchemyBase):
    __tablename__ = 'applications'
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, autoincrement=True)
    message_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True, nullable=False)
    by_user = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False)