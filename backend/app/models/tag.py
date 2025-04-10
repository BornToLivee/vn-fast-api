from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.associations import novel_tag


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    vndb_id = Column(String, nullable=True, unique=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True, unique=False)
    novels = relationship("Novel", secondary=novel_tag, back_populates="tags")