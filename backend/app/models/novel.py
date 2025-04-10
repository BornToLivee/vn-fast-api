from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Text, Date, Float, Enum, CheckConstraint
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.associations import novel_tag


class NovelStatus(str, PyEnum):
    READING = "READING"
    COMPLETED = "COMPLETED"
    DROPPED = "DROPPED"
    PLANNING = "PLANNING"


class NovelLanguage(str, PyEnum):
    RUSSIAN = "RUSSIAN"
    ENGLISH = "ENGLISH"
    UKRAINIAN = "UKRAINIAN"
    OTHER = "OTHER"


class Novel(Base):
    __tablename__ = "novels"
    __table_args__ = (
        CheckConstraint(
            "my_rating >= 0 AND my_rating <= 10", name="check_rating_range"
        ),
        {"extend_existing": True},
    )

    # My columns
    id = Column(Integer, primary_key=True)
    tags = relationship("Tag", secondary=novel_tag, back_populates="novels")
    my_review = Column(Text, nullable=True)
    status = Column(Enum(NovelStatus), default="READING")
    language = Column(Enum(NovelLanguage), default="russian")
    my_rating = Column(Float, nullable=True, unique=False)
    completed_date = Column(Date, nullable=True)
    # VNDB columns
    vndb_id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String)
    studio = Column(String)
    released = Column(Date)
    length = Column(Integer)  # from 1 to 5
    length_minutes = Column(Integer, nullable=True)
    votecount = Column(Integer)
    user_rating = Column(Integer, default=0)
