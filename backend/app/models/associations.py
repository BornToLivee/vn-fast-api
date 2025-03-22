from sqlalchemy import Table, ForeignKey, Column, Integer
from app.models.base import Base

novel_tag = Table(
    "novel_tag", Base.metadata,
    Column("novel_id", Integer, ForeignKey("novels.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)