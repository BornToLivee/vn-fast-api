from app.models.base import Base
from sqlalchemy import Column, ForeignKey, Integer, Table

novel_tag = Table(
    "novel_tag",
    Base.metadata,
    Column("novel_id", Integer, ForeignKey("novels.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
    extend_existing=True,
)
