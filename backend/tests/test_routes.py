import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
from datetime import datetime

from app.main import app
from app.database.settings import get_db
from app.models.base import Base
from app.models.novel import Novel

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    app.dependency_overrides[get_db] = override_get_db
    tear_down()
    Base.metadata.create_all(bind=engine)
    yield
    tear_down()

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def tear_down():
    Base.metadata.drop_all(bind=engine)


def mock_fetch_vndb_novel(vndb_id: str):
    if vndb_id == "v1":
        return {
            "id": "v1",
            "title": "Test Novel",
            "description": "Test description",
            "image": {"url": "https://example.com/test.jpg"},
            "developers": [{"name": "Test Studio"}],
            "released": "2022-01-01",
            "length": 100,
            "length_minutes": 120,
            "rating": 8.5,
            "votecount": 500
        }
    return None

def mock_search_vndb_novels_by_name(query: str):
    return [{
        "id": "v1",
        "title": "Test Novel",
        "description": "Test description",
        "image_url": "https://example.com/test.jpg",
        "studio": "Test Studio",
        "released": "2022-01-01",
        "length": 100,
        "length_minutes": 120,
        "rating": 8.5,
        "votecount": 500
    }]


@patch("app.api.novels.search_vndb_novels_by_name", side_effect=mock_search_vndb_novels_by_name)
def test_novel_search(mock_search):
    response = client.get("/novels/search/?query=test")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "v1"
    assert data[0]["title"] == "Test Novel"
    assert data[0]["image_url"] == "https://example.com/test.jpg"


def test_read_novels():
    tear_down()
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    novel = Novel(
        id=1,
        vndb_id="v1",
        title="Test Novel 1",
        description="Test description",
        image_url="https://example.com/1.jpg",
        studio="Test Developer",
        released=datetime.strptime("2022-01-01", "%Y-%m-%d").date(),
        length=100,
        length_minutes=120,
        user_rating=8.5,
        votecount=500,
        status="reading",
        language="russian",
        my_rating=8
    )
    session.add(novel)
    session.commit()
    session.close()

    response = client.get("/novels/")
    assert response.status_code == 200
    data = response.json()

    assert data[0]["title"] == "Test Novel 1"
    assert data[0]["status"] == "reading"
    assert len(data) == 1


def test_read_novels_empty():
    tear_down()
    Base.metadata.create_all(bind=engine)
 
    response = client.get("/novels/")
    assert response.status_code == 200
    assert response.json() == "No novels found yet"



def test_read_novel_detail():
    tear_down()
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    novel = Novel(
        id=10,
        vndb_id="v1",
        title="Test Novel 1",
        description="Test description",
        image_url="https://example.com/1.jpg",
        studio="Test Developer",
        released=datetime.strptime("2022-01-01", "%Y-%m-%d").date(),
        length=100,
        length_minutes=120,
        user_rating=8.5,
        votecount=500,
        status="reading",
        language="russian",
        my_rating=8
    )
    session.add(novel)
    session.commit()
    session.close()

    response = client.get("/novels/10")

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Novel 1"
    assert data["status"] == "reading"
    assert data["my_rating"] == 8
    assert data["tags"] == []
    assert data["language"] == "russian"
    assert data["description"] == "Test description"


def test_read_novel_detail_not_found():
    tear_down()
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    novel = Novel(
        id=10,
        vndb_id="v1",
        title="Test Novel 1",
        description="Test description",
        image_url="https://example.com/1.jpg",
        studio="Test Developer",
        released=datetime.strptime("2022-01-01", "%Y-%m-%d").date(),
        length=100,
        length_minutes=120,
        user_rating=8.5,
        votecount=500,
        status="reading",
        language="russian",
        my_rating=8
    )
    session.add(novel)
    session.commit()
    session.close()
    
    response = client.get("/novels/111")
    
    assert response.status_code == 404


@patch("app.api.novels.fetch_vndb_novel", side_effect=mock_fetch_vndb_novel)
def test_create_novel(mock_fetch_vndb_novel):
    tear_down()
    Base.metadata.create_all(bind=engine)
    
    novel_create = {
        "status": "reading",
        "my_review": "Great novel!",
        "my_rating": 9,
        "language": "russian",
        "tags": []
    }
    
    response = client.post("/novels/?vndb_id=v1", json={**novel_create})
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Novel"
    assert data["description"] == "Test description"
    assert data["studio"] == "Test Studio"
    assert data["released"] == "2022-01-01"
    assert data["status"] == "reading"
    assert data["language"] == "russian"
    assert data["my_review"] == "Great novel!"
    assert data["my_rating"] == 9
    assert len(data["tags"]) == 0


def test_create_novel_already_exists():
    tear_down()
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    novel = Novel(
        id=10,
        vndb_id="v1",
        title="Test Novel 1",
        description="Test description",
        image_url="https://example.com/1.jpg",
        studio="Test Developer",
        released=datetime.strptime("2022-01-01", "%Y-%m-%d").date(),
        length=100,
        length_minutes=120,
        user_rating=8.5,
        votecount=500,
        status="reading",
        language="russian",
        my_rating=8
    )
    session.add(novel)
    session.commit()
    session.close()

    response = client.post("/novels/?vndb_id=v1", json={
        "status": "reading",
        "my_review": "Good novel!",
        "my_rating": 7,
        "language": "english",
        "tags": []
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "Novel already exists"}