from typing import Optional

from pydantic import BaseModel, EmailStr, UUID4

# Shared properties
class WebhookBase(BaseModel):
    url: Optional[str] = None


# Properties to receive via API on creation
class WebhookCreate(WebhookBase):
    url: str


# Properties to receive via API on update
class WebhookUpdate(WebhookBase):
    alias: Optional[str] = None
    active: Optional[bool] = True


class WebhookInDBBase(WebhookBase):
    id: Optional[UUID4] = None
    url: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class WebhookInDB(WebhookInDBBase):
    pass

class Webhook(WebhookInDBBase):
    pass