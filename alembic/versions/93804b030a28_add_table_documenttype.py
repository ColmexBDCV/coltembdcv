"""Add table DocumentType

Revision ID: 93804b030a28
Revises: 511fe81bf7a8
Create Date: 2024-10-15 10:57:49.926014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93804b030a28'
down_revision: Union[str, None] = '511fe81bf7a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type_name', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    sa.Column('fecha_modificacion', sa.DateTime(), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['user_auth.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type'),
    sa.UniqueConstraint('type_name')
    )
    op.create_index(op.f('ix_document_types_id'), 'document_types', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_document_types_id'), table_name='document_types')
    op.drop_table('document_types')
    # ### end Alembic commands ###
