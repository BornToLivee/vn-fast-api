import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock
from app.services.vndb import search_vndb_novels_by_name, fetch_vndb_novel
from app.models.novel import Novel
from app.schemas.novel import NovelCreate, NovelSearchResponse
from sqlalchemy.orm import Session
from unittest.mock import AsyncMock

client = TestClient(app)

@pytest.fixture
def mock_search_vndb_novels_by_name(mocker):
    async def mock_search(*args, **kwargs):
        return [
            NovelSearchResponse(id="v7", image_url="https://t.vndb.org/cv/48/90048.jpg", title="Tsukihime"),
            NovelSearchResponse(id="v20", image_url="https://t.vndb.org/cv/20/90020.jpg", title="Fate/Stay Night")
        ]
    
    # Изменяем путь для патча
    return mocker.patch("app.api.novels.search_vndb_novels_by_name", side_effect=mock_search)


@pytest.fixture
def mock_fetch_vndb_novel(mocker):
    mock_data = {
        "id": "1",
        "title": "Test Novel 1",
        "description": "Test description",
        "image": {"url": "https://example.com/1.jpg"},
        "developers": [{"name": "Test Developer"}],
        "released": "2022-01-01",
        "length": 100,
        "length_minutes": 120,
        "rating": 8.5,
        "votecount": 500,
    }
    return mocker.patch("app.api.novels.fetch_vndb_novel", return_value=mock_data)


@pytest.mark.asyncio
async def test_novel_search(mock_search_vndb_novels_by_name):
    response = client.get("/novels/search?query=Test")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 2
    assert data[0]["id"] == "v7"
    assert data[0]["title"] == "Tsukihime"
    assert data[1]["id"] == "v20"
    assert data[1]["title"] == "Fate/Stay Night"


def test_read_novels(test_db):
    response = client.get("/novels/?skip=0&limit=10")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_read_novel(test_db, mock_fetch_vndb_novel):
    novel_data = {
        "status": "reading",
        "my_review": "Test review",
        "my_rating": 8,
        "language": "English",
        "tags": []
    }
    
    create_response = client.post("/novels/?vndb_id=1", json=novel_data)
    print("Create response:", create_response.json())
    
    novels_response = client.get("/novels/")
    created_novel = novels_response.json()[0]
    created_novel_id = created_novel["id"]
    
    response = client.get(f"/novels/{created_novel_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_novel_id
    assert data["title"] == "Test Novel 1"
    assert data["status"] == "reading"


def test_create_novel(test_db, mock_fetch_vndb_novel):
    novel_data = {
        "status": "reading",
        "my_review": "Interesting novel",
        "my_rating": 8,
        "language": "English",
        "tags": []
    }
    
    response = client.post("/novels/?vndb_id=1", json=novel_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Novel 1"
    assert data["status"] == novel_data["status"]
    assert data["my_review"] == novel_data["my_review"]
    assert data["my_rating"] == novel_data["my_rating"]


def test_create_novel_already_exists(test_db, mock_fetch_vndb_novel):
    novel_data = {
        "status": "reading",
        "my_review": "First review",
        "my_rating": 8,
        "language": "English",
        "tags": []
    }
    
    first_response = client.post("/novels/?vndb_id=1", json=novel_data)
    assert first_response.status_code == 200
    
    second_response = client.post("/novels/?vndb_id=1", json=novel_data)
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Novel already exists"


def test_create_novel_vndb_not_found(test_db, mock_fetch_vndb_novel):
    mock_fetch_vndb_novel.return_value = None
    
    novel_data = {
        "status": "reading",
        "my_review": "Interesting novel",
        "my_rating": 8,
        "language": "English",
        "tags": []
    }
    
    response = client.post("/novels/?vndb_id=999", json=novel_data)  # vndb_id только в URL
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Novel details not found"