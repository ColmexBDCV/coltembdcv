"""Change map table

Revision ID: 73fe2daaf621
Revises: e3aa90470eda
Create Date: 2024-10-31 03:20:15.004117

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Identificadores de revisión
revision: str = '73fe2daaf621'
down_revision: Union[str, None] = 'e3aa90470eda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Alterar tabla map_filters
    with op.batch_alter_table('map_filters', schema=None) as batch_op:
        # Crear la nueva restricción sin intentar eliminar la previa en SQLite
        batch_op.create_foreign_key("fk_map_filters_user_auth_user_id", "user_auth", ["user_id"], ["id"])

    # Alterar tabla maps
    with op.batch_alter_table('maps', schema=None) as batch_op:
        # Crear la nueva restricción sin intentar eliminar la previa en SQLite
        batch_op.create_foreign_key("fk_maps_user_auth_user_id", "user_auth", ["user_id"], ["id"])

def downgrade() -> None:
    # Revertir en maps
    with op.batch_alter_table('maps', schema=None) as batch_op:
        batch_op.drop_constraint("fk_maps_user_auth_user_id", type_='foreignkey')
        batch_op.create_foreign_key("fk_maps_user_info_user_id", "user_info", ["user_id"], ["id"])

    # Revertir en map_filters
    with op.batch_alter_table('map_filters', schema=None) as batch_op:
        batch_op.drop_constraint("fk_map_filters_user_auth_user_id", type_='foreignkey')
        batch_op.create_foreign_key("fk_map_filters_user_info_user_id", "user_info", ["user_id"], ["id"])
