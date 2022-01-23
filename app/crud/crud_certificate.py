from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.certificate import Certificate
from app.schemas.certificate import CertificateCreateInDB, CertificateUpdate


class CRUDItem(CRUDBase[Certificate, CertificateCreateInDB, CertificateUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: CertificateCreateInDB, user_id: str
    ) -> Certificate:
        obj_in_data = jsonable_encoder(obj_in)
        print(obj_in_data)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_user(
        self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Certificate]:
        return (
            db.query(self.model)
            .filter(Certificate.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

certificate = CRUDItem(Certificate)