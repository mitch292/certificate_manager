from typing import Optional
from datetime import datetime

from pydantic import BaseModel, UUID4

# Shared properties
class CertificateBase(BaseModel):
    alias: Optional[str] = None


# Properties to receive via API on creation
class CertificateCreate(CertificateBase):
    alias: str


# Properties to receive via API on update
class CertificateUpdate(CertificateBase):
    alias: Optional[str] = None
    active: Optional[bool] = True

class CertificateCreateInDB(CertificateBase):
    private_key: bytes
    active: bool
    expires_at: str
    certificate_body: bytes
    private_key: bytes

class CertificateInDBBase(CertificateBase):
    id: Optional[UUID4] = None
    active: bool
    expires_at: datetime
    certificate_body: bytes
    class Config:
        orm_mode = True


# Additional properties to return via API
class Certificate(CertificateInDBBase):
    pass


# Additional properties stored in DB
class CertificateInDB(CertificateInDBBase):
    private_key: bytes