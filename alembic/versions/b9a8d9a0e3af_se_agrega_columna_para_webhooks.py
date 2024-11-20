"""Se agrega columna para webhooks

Revision ID: b9a8d9a0e3af
Revises: 73fe2daaf621
Create Date: 2024-11-05 14:54:21.383408

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9a8d9a0e3af'
down_revision: Union[str, None] = '73fe2daaf621'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Agregar columnas con un valor predeterminado temporal
    op.add_column('sites', sa.Column('contacto_webhook', sa.String(), nullable=False, server_default="https://redescolmex.webhook.office.com/webhookb2/f5f44f0f-371e-4c95-b39d-4da3e230bb4e@93db1ea2-0b31-43e8-aece-2228fabb7af1/IncomingWebhook/8bbfaaeaaee34e458e2e0510acf92eef/811356f3-d509-4767-9780-a7bf281c13b6/V2Reivy6bmOBZ1Fd26f4G3MUZqcdi6ieE3EYHYfS4IXW41"))
    op.add_column('sites', sa.Column('monitor_webhook', sa.String(), nullable=False, server_default="https://redescolmex.webhook.office.com/webhookb2/f5f44f0f-371e-4c95-b39d-4da3e230bb4e@93db1ea2-0b31-43e8-aece-2228fabb7af1/IncomingWebhook/8bbfaaeaaee34e458e2e0510acf92eef/811356f3-d509-4767-9780-a7bf281c13b6/V2Reivy6bmOBZ1Fd26f4G3MUZqcdi6ieE3EYHYfS4IXW41"))



def downgrade() -> None:
    # Eliminar las columnas agregadas en la migración
    op.drop_column('sites', 'monitor_webhook')
    op.drop_column('sites', 'contacto_webhook')