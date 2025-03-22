from sqlalchemy import Column, Integer, String, Text, Date, Float
from sqlalchemy.orm import relationship

from app.models.base import Base
from backend.app.models.associations import novel_tag

class Novel(Base):
    __tablename__ = "novels"
    # My columns
    id = Column(Integer, primary_key=True)
    tags = relationship("Tag", secondary=novel_tag, back_populates="novels")
    my_review = Column(Text, nullable=True)
    status = Column(String, default="reading")
    language = Column(String, default="russian")
    my_rating = Column(Float, nullable=True, unique=False)
    # VNDB columns
    vndb_id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String)
    studio = Column(String)
    released = Column(Date)
    length = Column(Integer) # from 1 to 5
    length_minutes = Column(Integer, nullable=True)
    votecount = Column(Integer)  # "reading" или "completed"
    user_rating = Column(Integer, default=0)