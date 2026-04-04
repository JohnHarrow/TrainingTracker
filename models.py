from sqlalchemy import Column, Integer, String
from database import Base


class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    type = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    notes = Column(String, nullable=False)