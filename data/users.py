import datetime
from sqlalchemy import orm, Column, String, DateTime, Integer
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from flask_login import UserMixin

class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=True)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    position = Column(String, nullable=True)
    speciality = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String, index=True, unique=True, nullable=True)
    modified_date = Column(DateTime, default=datetime.datetime.now)
    hashed_password = Column(String, nullable=True)
    jobs = orm.relationship("Jobs", back_populates='user')



    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
