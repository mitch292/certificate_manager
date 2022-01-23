# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.certificate import Certificate  # noqa
from app.models.user import User  # noqa
from app.models.webhook import Webhook  # noqa
