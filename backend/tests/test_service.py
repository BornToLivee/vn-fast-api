import pytest
import httpx
import requests
from unittest.mock import AsyncMock
from backend.app.services.vndb import search_vndb_novels_by_name, fetch_vndb_novel

@pytest.mark.asyncio
async def test_search_vndb_novels_by_name(mocker):
    mock_response = {
        "results": [
            {"id": "1", "title": "Test Novel 1", "image": {"url": "https://example.com/1.jpg"}},
            {"id": "2", "title": "Test Novel 2", "image": {"url": "https://example.com/2.jpg"}},
        ]
    }

    mock_post = mocker.patch("httpx.AsyncClient.post", new_callable=AsyncMock)
    mock_post.return_value.status_code = 200
    mock_post.return_value.json = lambda: mock_response  # Просто возвращаем словарь

    # Вызываем асинхронную функцию
    result = await search_vndb_novels_by_name("Test")
    
    # Проверка результата
    assert len(result) == 2
    assert result[0].id == "1"
    assert result[0].title == "Test Novel 1"
    assert result[0].image_url == "https://example.com/1.jpg"



def test_fetch_vndb_novel(mocker):
    mock_response = {
        "results": [
            {
                "id": "1",
                "title": "Test Novel 1",
                "released": "2022-01-01",
                "image": {"url": "https://example.com/1.jpg"},
                "length": 3,
                "length_minutes": 120,
                "description": "Test description",
                "rating": 8.5,
                "votecount": 100,
                "developers": [{"name": "Test Studio"}]
            }
        ]
    }
    
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = mock_response
    
    result = fetch_vndb_novel("1")
    
    assert result is not None
    assert result["id"] == "1"
    assert result["title"] == "Test Novel 1"
    assert result["description"] == "Test description"
    assert result["image"]["url"] == "https://example.com/1.jpg"
    assert result["developers"][0]["name"] == "Test Studio"
