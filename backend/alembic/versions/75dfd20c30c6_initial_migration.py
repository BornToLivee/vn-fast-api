"""Initial migration

Revision ID: 75dfd20c30c6
Revises:
Create Date: 2025-03-31 13:46:43.327643

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "75dfd20c30c6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
