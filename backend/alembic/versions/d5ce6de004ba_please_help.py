"""please help

Revision ID: d5ce6de004ba
Revises: 25888e90bb01
Create Date: 2025-03-31 14:42:56.411632

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d5ce6de004ba"
down_revision: Union[str, None] = "25888e90bb01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Сначала удаляем существующие enum типы, если они есть
    op.execute("DROP TYPE IF EXISTS novelstatus")
    op.execute("DROP TYPE IF EXISTS novellanguage")

    # Создаем enum типы заново
    op.execute(
        "CREATE TYPE novelstatus AS ENUM ('READING', 'COMPLETED', 'DROPPED', 'PLANNING')"
    )
    op.execute(
        "CREATE TYPE novellanguage AS ENUM ('RUSSIAN', 'ENGLISH', 'UKRAINIAN', 'OTHER')"
    )

    # Добавляем новую колонку
    op.add_column("novels", sa.Column("completed_date", sa.Date(), nullable=True))

    # Обновляем существующие значения
    op.execute("UPDATE novels SET status = upper(status)")
    op.execute("UPDATE novels SET language = upper(language)")

    # Изменяем тип колонок с явным приведением
    op.execute(
        "ALTER TABLE novels ALTER COLUMN status TYPE novelstatus USING status::novelstatus"
    )
    op.execute(
        "ALTER TABLE novels ALTER COLUMN language TYPE novellanguage USING language::novellanguage"
    )


def downgrade() -> None:
    # Возвращаем к строковым типам
    op.execute("ALTER TABLE novels ALTER COLUMN status TYPE varchar")
    op.execute("ALTER TABLE novels ALTER COLUMN language TYPE varchar")

    # Удаляем enum типы
    op.execute("DROP TYPE IF EXISTS novelstatus")
    op.execute("DROP TYPE IF EXISTS novellanguage")

    op.drop_column("novels", "completed_date")
