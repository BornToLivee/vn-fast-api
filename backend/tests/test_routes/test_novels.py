from unittest.mock import patch
from datetime import datetime

from app.models.novel import Novel


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
def test_novel_search(mock_search, client):
    response = client.get("/novels/search/?query=test")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "v1"
    assert data[0]["title"] == "Test Novel"
    assert data[0]["image_url"] == "https://example.com/test.jpg"


def test_read_novels(client, db):
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
        status="READING",
        language="RUSSIAN",
        my_rating=8.0
    )
    db.add(novel)
    db.commit()

    response = client.get("/novels/")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["title"] == "Test Novel 1"
    assert data[0]["status"] == "READING"
    assert len(data) == 1


def test_read_novels_empty(client):
    response = client.get("/novels/")
    assert response.status_code == 200
    assert response.json() == "No novels found yet"


def test_read_novel_detail(client, db):
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
        status="READING",
        language="RUSSIAN",
        my_rating=8.0
    )
    db.add(novel)
    db.commit()

    response = client.get("/novels/10")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Novel 1"
    assert data["status"] == "READING"
    assert data["my_rating"] == 8.0
    assert data["tags"] == []
    assert data["language"] == "RUSSIAN"
    assert data["description"] == "Test description"


def test_read_novel_detail_not_found(client, db):
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
        status="READING",
        language="RUSSIAN",
        my_rating=8.0
    )
    db.add(novel)
    db.commit()

    response = client.get("/novels/111")
    assert response.status_code == 404


@patch("app.api.novels.fetch_vndb_novel", side_effect=mock_fetch_vndb_novel)
def test_create_novel(mock_fetch_vndb_novel, client):
    novel_create = {
        "status": "READING",
        "my_review": "Great novel!",
        "my_rating": 9.0,
        "language": "RUSSIAN",
    }

    response = client.post("/novels/?vndb_id=v1", json=novel_create)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Novel"
    assert data["description"] == "Test description"
    assert data["studio"] == "Test Studio"
    assert data["released"] == "2022-01-01"
    assert data["status"] == "READING"
    assert data["language"] == "RUSSIAN"
    assert data["my_review"] == "Great novel!"
    assert data["my_rating"] == 9.0

def test_create_novel_already_exists(client, db):
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
        status="READING",
        language="RUSSIAN",
        my_rating=8.0
    )
    db.add(novel)
    db.commit()

    response = client.post("/novels/?vndb_id=v1", json={
        "status": "READING",
        "my_review": "Good novel!",
        "my_rating": 7.0,
        "language": "RUSSIAN",
        "tags": []
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "Novel already exists"}