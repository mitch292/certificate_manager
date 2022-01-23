import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .webhook import Webhook  # noqa: F401
    from .user import User  # noqa: F401

class Certificate(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    alias = Column(String, nullable=False)
    private_key = Column(Text, nullable=False)
    certificate_body = Column(Text, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    active = Column(Boolean, nullable=False)
    user = relationship("User", back_populates="certificates")
    webhooks = relationship("Webhook", back_populates="certificate")
