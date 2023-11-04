"""add content column to post table"

Revision ID: 9582a8906a8c
Revises: b031a8290eb0
Create Date: 2023-11-04 17:35:57.482703

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9582a8906a8c'
down_revision: Union[str, None] = 'b031a8290eb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
