# conftest.py
import logging
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.settings import get_db
from app.models.base import Base

from app.repositories.novels import NovelRepository
from app.repositories.tags import TagRepository
from app.services.novel import NovelService
from app.services.tag import TagService
from app.services.vndb import VNDBService


# Disable logging during tests
logging.disable(logging.CRITICAL)

# Test database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """
    Create a fresh database session for each test.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """
    Create a test client with a fresh database session.
    """

    def override_get_db():
        try:
            yield db
        finally:
            pass

    # Override dependencies for services and repositories
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[NovelRepository] = lambda: NovelRepository(db=db)
    app.dependency_overrides[TagRepository] = lambda: TagRepository(db=db)
    app.dependency_overrides[VNDBService] = lambda: VNDBService(db=db)
    app.dependency_overrides[TagService] = lambda: TagService(
        db=db, repo=TagRepository(db=db)
    )
    app.dependency_overrides[NovelService] = lambda: NovelService(
        db=db,
        repo=NovelRepository(db=db),
        vndb_service=VNDBService(db=db),
        tag_service=TagService(db=db, repo=TagRepository(db=db)),
    )

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
