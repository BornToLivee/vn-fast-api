"""add vndb_id column in tags model

Revision ID: 83f32438a9f3
Revises: 74910184b72d
Create Date: 2025-04-10 13:48:00.890222

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "83f32438a9f3"
down_revision: Union[str, None] = "74910184b72d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("tags", sa.Column("vndb_id", sa.String(), nullable=True))
    op.create_unique_constraint(None, "tags", ["vndb_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "tags", type_="unique")
    op.drop_column("tags", "vndb_id")
    # ### end Alembic commands ###
