"""Add metadatos table

Revision ID: 15aae72c9a5b
Revises: acf1a20bdf9c
Create Date: 2024-11-20 14:55:02.069765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15aae72c9a5b'
down_revision: Union[str, None] = 'acf1a20bdf9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
