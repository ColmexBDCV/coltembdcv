"""Add maps relationship to UserInfo

Revision ID: e3aa90470eda
Revises: 0b65334bdfad
Create Date: 2024-10-31 03:08:50.260699

"""
from alembic import op
from typing import Union, Sequence

# revision identifiers, used by Alembic.
revision: str = 'e3aa90470eda'
down_revision: Union[str, None] = '0b65334bdfad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    with op.batch_alter_table('map_filters', schema=None) as batch_op:
        # Crea la nueva clave externa sin eliminar la anterior
        batch_op.create_foreign_key("fk_map_filters_user_auth_user_id", "user_auth", ["user_id"], ["id"])

    with op.batch_alter_table('maps', schema=None) as batch_op:
        # Crea la nueva clave externa sin eliminar la anterior
        batch_op.create_foreign_key("fk_maps_user_auth_user_id", "user_auth", ["user_id"], ["id"])

def downgrade() -> None:
    with op.batch_alter_table('maps', schema=None) as batch_op:
        batch_op.drop_constraint("fk_maps_user_auth_user_id", type_='foreignkey')
        batch_op.create_foreign_key("fk_maps_user_info_user_id", "user_info", ["user_id"], ["id"])

    with op.batch_alter_table('map_filters', schema=None) as batch_op:
        batch_op.drop_constraint("fk_map_filters_user_auth_user_id", type_='foreignkey')
        batch_op.create_foreign_key("fk_map_filters_user_info_user_id", "user_info", ["user_id"], ["id"])