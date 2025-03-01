import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.core.database import DBBase


class User(DBBase):
    """
    Database model for users
    """

    __tablename__ = "users"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    gender = Column(
        Enum("MALE", "FEMALE", "OTHER", name="enum_genders"),
        nullable=True,
    )
    medical_id = Column(String(12), nullable=True)
    hospital_id = Column(
        Integer, ForeignKey("hospitals.id", ondelete="SET NULL"), nullable=True
    )
    dob = Column(Date, nullable=False)
    country = Column(String(2), nullable=False)
    account_type = Column(
        Enum("INDIVIDUAL", "PRACTITIONER", "ORGANIZATION", name="enum_account_types"),
        nullable=True,
    )
    criipto_sub = Column(String(50), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
