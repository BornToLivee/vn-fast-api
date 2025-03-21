from sqlalchemy import Column, Integer, String, Table, ForeignKey
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
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True, unique=False)
    my_rating = Column(Integer, nullable=True, unique=False)
    tags = relationship("Tag", secondary="novel_tag", back_populates="novels")


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