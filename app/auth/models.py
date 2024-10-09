from datetime import datetime
from typing import cast
from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.core.database import DBBase


class OAuth2UserLoginAttempt(DBBase):
    """
    Database model for oauth2 login attempts
    """

    __tablename__ = "oauth2_user_login_attempts"

    id = cast(int, Column(Integer, primary_key=True, autoincrement=True))
    service = cast(str, Column(String(20), nullable=False))
    state_token = cast(str, Column(String(10), unique=True, nullable=False))
    redirect_url = cast(str, Column(String, nullable=False))
    is_used = cast(bool, Column(Boolean, default=False, nullable=False))
    created_at = cast(
        datetime, Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    )
    expires_at = cast(datetime, Column(DateTime(timezone=True), nullable=False))


class RefreshToken(DBBase):
    """
    Database model for refresh tokens
    """

    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(10), nullable=False)
    content = Column(String, nullable=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
