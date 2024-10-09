from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from app.core.database import DBBase


class Hospital(DBBase):
    """
    Database model for hospitals
    """

    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    address = Column(String(500), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
