from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.webhook import Webhook
from app.schemas.webhook import WebhookCreate, WebhookUpdate


class CRUDItem(CRUDBase[Webhook, WebhookCreate, WebhookUpdate]):
    def create_with_certificate(
        self, db: Session, *, obj_in: WebhookCreate, certificate_id: str
    ) -> Webhook:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, certificate_id=certificate_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_certificate(
        self, db: Session, *, certificate_id: str, skip: int = 0, limit: int = 100
    ) -> List[Webhook]:
        return (
            db.query(self.model)
            .filter(Webhook.certificate_id == certificate_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


webhook = CRUDItem(Webhook)