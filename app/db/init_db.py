from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import (
    DEFAULT_USER_NAME,
    DEFAULT_USER_EMAIL,
    DEFAULT_USER_PASSWORD,
)
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations

    user = crud.user.get_by_email(db, email=DEFAULT_USER_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            name=DEFAULT_USER_NAME,
            email=DEFAULT_USER_EMAIL,
            password=DEFAULT_USER_PASSWORD,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841