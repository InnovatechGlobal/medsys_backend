from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.core.database import DBBase


class OAuth2UserLoginAttempt(DBBase):
    """
    Database model for oauth2 login attempts
    """

    __tablename__ = "oauth2_user_login_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service = Column(String(10), nullable=False)
    state_token = Column(String(10), unique=True, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
