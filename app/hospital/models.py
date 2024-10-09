from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

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


class HospitalStaff(DBBase):
    """
    Database model for hospital staff
    """

    __tablename__ = "hospital_staff"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hospital_id = Column(
        Integer, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,  # User can only be a staff to one hospital
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
