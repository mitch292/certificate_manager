from typing import Any, List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.service import CertificateGenerator, CertificateManager, send_webhook

router = APIRouter()

@router.get("/{user_id}/certificates", response_model=List[schemas.Certificate])
def read_certificates(
    user_id: str,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve certificates for a user.
    """
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist.",
        )
    certificates = crud.certificate.get_multi_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return certificates


@router.post("/{user_id}/certificates", response_model=schemas.Certificate, status_code=status.HTTP_201_CREATED)
def create_certificate(
    user_id: str,
    *,
    db: Session = Depends(deps.get_db),
    certificate_in: schemas.CertificateCreate,
) -> Any:
    """
    Create a new certificate.
    """
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist.",
        )

    generated_cert = CertificateGenerator(user, certificate_in.alias)
    certificate = crud.certificate.create_with_user(db, obj_in=generated_cert.to_dict(), user_id=user.id)

    return certificate


@router.get("/{user_id}/certificates/{certificate_id}", response_model=schemas.Certificate)
def get_certificate_by_id(
    user_id: str,
    certificate_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific certificate by id.
    """
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist.",
        )

    certificate = crud.certificate.get(db, id=certificate_id)
    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="The certificate does not exist.",
        )

    return certificate


@router.put("/{user_id}/certificates/{certificate_id}", response_model=schemas.Certificate)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: str,
    certificate_id: str,
    certificate_in: schemas.CertificateUpdate,
    background_tasks: BackgroundTasks,
) -> Any:
    """
    Update a certificate.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    certificate = crud.certificate.get(db, id=certificate_id)
    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="The certificate with this username does not exist in the system",
        )
    updated_cert = crud.certificate.update(db, db_obj=certificate, obj_in=certificate_in)
    cert_manager = CertificateManager(db, certificate)
    webhooks = cert_manager.get_webhooks_to_notify()
    for webhook in webhooks:
        background_tasks.add_task(send_webhook, url=webhook.url, cert=updated_cert)

    return updated_cert