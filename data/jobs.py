import datetime
from sqlalchemy import orm, Column, String, DateTime, Integer, Boolean, ForeignKey
from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job = Column(String, nullable=True)
    work_size = Column(Integer, default=0)
    collaborators = Column(String, nullable=True)
    start_date = Column(DateTime, default=datetime.datetime.now)
    end_date = Column(DateTime, default=datetime.datetime.now)
    is_finished = Column(Boolean, default=True)
    team_leader = Column(Integer, ForeignKey("users.id"))
    orm.relationship("User")

    def __repr__(self):
        return f"{self.id} {self.job}"