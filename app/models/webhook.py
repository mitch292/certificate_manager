import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .certificate import Certificate  # noqa: F401

class Webhook(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    certificate_id = Column(UUID(as_uuid=True), ForeignKey('certificate.id'), nullable=False)
    url = Column(String, nullable=False)
    certificate = relationship("Certificate", back_populates="webhooks")
