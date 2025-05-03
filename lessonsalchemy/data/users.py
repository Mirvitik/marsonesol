import sqlalchemy
from flask_login import UserMixin
from itsdangerous import Serializer
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    astropass = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)
    cap_id = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city_from = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cap_pass = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)

    def check_password(self, passw, passw2):
        if passw == self.cap_pass and passw2 == self.astropass:
            return True
        return False
