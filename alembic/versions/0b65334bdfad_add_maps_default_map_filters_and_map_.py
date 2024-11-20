"""Add maps, default_map_filters, and map_filters tables v2

Revision ID: 0b65334bdfad
Revises: 971776e04f4e
Create Date: 2024-10-31 01:19:37.920608

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b65334bdfad'
down_revision: Union[str, None] = '971776e04f4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('default_map_filters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filter_key', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('filter_key')
    )
    op.create_index(op.f('ix_default_map_filters_id'), 'default_map_filters', ['id'], unique=False)
    op.create_table('map_filters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('site_id', sa.Integer(), nullable=False),
    sa.Column('id_filter_map_default', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('date_creation', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('date_modification', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_filter_map_default'], ['default_map_filters.id'], ),
    sa.ForeignKeyConstraint(['site_id'], ['sites.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_map_filters_id'), 'map_filters', ['id'], unique=False)
    op.create_table('maps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('facet', sa.String(), nullable=False),
    sa.Column('facet_value', sa.String(), nullable=False),
    sa.Column('site_id', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('date_creation', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('date_modification', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['site_id'], ['sites.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_maps_id'), 'maps', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_maps_id'), table_name='maps')
    op.drop_table('maps')
    op.drop_index(op.f('ix_map_filters_id'), table_name='map_filters')
    op.drop_table('map_filters')
    op.drop_index(op.f('ix_default_map_filters_id'), table_name='default_map_filters')
    op.drop_table('default_map_filters')
    # ### end Alembic commands ###
