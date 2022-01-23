from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get(
    "/{user_id}/certificates/{certificate_id}/webhooks",
    response_model=List[schemas.Webhook],
)
def read_webhook(
    user_id: str,
    certificate_id: str,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve webhooks for a certificate.
    """
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist.",
        )
    certificate = crud.certificate.get(db, certificate_id)
    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="The certificate does not exist.",
        )
    webhooks = crud.webhook.get_multi_by_certificate(
        db, certificate_id=certificate_id, skip=skip, limit=limit
    )
    return webhooks


@router.post(
    "/{user_id}/certificates/{certificate_id}/webhooks",
    response_model=schemas.Webhook,
    status_code=status.HTTP_201_CREATED,
)
def create_webhook(
    user_id: str,
    certificate_id: str,
    *,
    db: Session = Depends(deps.get_db),
    webhook_in: schemas.WebhookCreate,
) -> Any:
    """
    Create a new webhook.
    """
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist.",
        )
    certificate = crud.certificate.get(db, certificate_id)
    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="The certificate does not exist.",
        )

    webhook = crud.webhook.create_with_certificate(
        db, obj_in=webhook_in, certificate_id=certificate_id
    )

    return webhook


@router.get(
    "/{user_id}/certificates/{certificate_id}/webhooks/{webhook_id}",
    response_model=schemas.Webhook,
)
def get_webhook_by_id(
    user_id: str,
    certificate_id: str,
    webhook_id: str,
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
    certificate = crud.certificate.get(db, certificate_id)
    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="The certificate does not exist.",
        )
    webhook = crud.webhook.get(db, webhook_id)
    if not webhook:
        raise HTTPException(
            status_code=404,
            detail="The webhook does not exist.",
        )

    return webhook


@router.delete(
    "/{user_id}/certificates/{certificate_id}/webhooks/{webhook_id}",
    response_model=schemas.Webhook,
)
def delete_webhook(
    *,
    db: Session = Depends(deps.get_db),
    user_id: str,
    certificate_id: str,
    webhook_id: str,
) -> Any:
    """
    Delete a webhook.
    """
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist.",
        )
    certificate = crud.certificate.get(db, certificate_id)
    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="The certificate does not exist.",
        )
    webhook = crud.webhook.get(db, webhook_id)
    if not webhook:
        raise HTTPException(
            status_code=404,
            detail="The webhook does not exist.",
        )

    crud.webhook.remove(db, webhook_id)

    return webhook
