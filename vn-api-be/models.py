from sqlalchemy import Column, Integer, String, Table, ForeignKey, Text, Date, Float
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


novel_tag = Table(
    "novel_tag", Base.metadata,
    Column("user_id", Integer, ForeignKey("novels.id")),
    Column("tags_id", Integer, ForeignKey("tags.id"))
)

class Novel(Base):
    __tablename__ = "novels"
    # My columns
    id = Column(Integer, primary_key=True)
    tags = relationship("Tag", secondary="novel_tag", back_populates="novels")
    my_review = Column(Text, nullable=True)
    status = Column(String, default="reading")
    language = Column(String, default="russian")
    my_rating = Column(Integer, nullable=True, unique=False)
    # VNDB columns
    vndb_id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String)
    studio = Column(String)
    released = Column(Date)
    length = Column(Integer) # from 1 to 5
    length_minutes = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)
    votecount = Column(Integer)  # "reading" или "completed"
    user_rating = Column(Integer, default=0)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True, unique=False)
    novels = relationship("Novel", secondary="novel_tag", back_populates="tags")


DATABASE_URL = "sqlite:///./testnovels.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)