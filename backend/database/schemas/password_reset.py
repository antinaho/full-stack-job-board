from sqlalchemy import Column, Integer, Uuid, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from backend.database.core import Base
from sqlalchemy.dialects.postgresql import UUID


class PasswordReset(Base):
    __tablename__ = "password_reset_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    reset_token = Column(String())
    expirary_time = Column(DateTime)

    user = relationship("User", back_populates="password_reset_req")
