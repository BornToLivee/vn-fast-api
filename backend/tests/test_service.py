import pytest
from unittest.mock import AsyncMock
from backend.app.services.vndb import search_vndb_novels_by_name, fetch_vndb_novel, fetch_vndb_novel_tags, fetch_vndb_tags_description

@pytest.mark.asyncio
async def test_search_vndb_novels_by_name(mocker):
    mocker.patch("watchtower.CloudWatchLogHandler")
    mock_response = {
        "results": [
            {"id": "1", "title": "Test Novel 1", "image": {"url": "https://example.com/1.jpg"}},
            {"id": "2", "title": "Test Novel 2", "image": {"url": "https://example.com/2.jpg"}},
        ]
    }

    mock_post = mocker.patch("httpx.AsyncClient.post", new_callable=AsyncMock)
    mock_post.return_value.status_code = 200
    mock_post.return_value.json = lambda: mock_response 

    result = await search_vndb_novels_by_name("Test")
    
    assert len(result) == 2
    assert result[0].id == "1"
    assert result[0].title == "Test Novel 1"
    assert result[0].image_url == "https://example.com/1.jpg"


def test_fetch_vndb_novel(mocker):
    mocker.patch("watchtower.CloudWatchLogHandler")
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


@pytest.mark.asyncio
async def test_fetch_vndb_novel_tags(mocker):
    mocker.patch("watchtower.CloudWatchLogHandler")
    
    mock_response = {
        "results": [
            {   "id": "v1",
                "tags": [
                    {
                        "id": "g32",
                        "name": "ADV",
                        "category": "tech",
                        "rating": 2.764706,
                        "spoiler": 0
                    },
                    {
                        "id": "g133",
                        "name": "Male Protagonist",
                        "category": "cont",
                        "rating": 2.9375,
                        "spoiler": 0
                    },
                    {
                        "id": "g236",
                        "name": "Low Sexual Content",
                        "category": "ero",
                        "rating": 2.5555556,
                        "spoiler": 0
                    },
                    {
                        "id": "g160",
                        "name": "Bloody Scenes",
                        "category": "cont",
                        "rating": 1.4,
                        "spoiler": 2
                    },
                    {
                        "id": "g176",
                        "name": "Foolish Friend",
                        "category": "cont",
                        "rating": 0.21428572,
                        "spoiler": 0
                    }
                ]
            }
        ]
    }
    
    mock_response_obj = mocker.patch("httpx.AsyncClient.post", new_callable=AsyncMock)
    mock_response_obj.return_value.status_code = 200
    mock_response_obj.return_value.json = lambda: mock_response 

    mock_fetch_description = mocker.patch("backend.app.services.vndb.fetch_vndb_tags_description")
    mock_fetch_description.return_value = "Test description"

    result = await fetch_vndb_novel_tags("v1")
    
    assert len(result) == 2
    assert result[0]["vndb_id"] == "g32"
    assert result[0]["name"] == "ADV"
    assert result[0]["description"] == "Test description"
    
    assert result[1]["vndb_id"] == "g133"
    assert result[1]["name"] == "Male Protagonist"
    assert result[1]["description"] == "Test description"
    
    mock_response_obj.assert_called_once()
    mock_fetch_description.assert_has_calls([
        mocker.call("g32"),
        mocker.call("g133")
    ])
    
    call_args = mock_response_obj.call_args[1]
    assert "json" in call_args
    assert call_args["json"]["filters"] == ["id", "=", "v1"]
    assert call_args["json"]["fields"] == "tags.rating, tags.name, tags.category, tags.spoiler"


@pytest.mark.asyncio
async def test_fetch_vndb_novel_tags_api_error(mocker):
    mocker.patch("watchtower.CloudWatchLogHandler")
    
    mock_post = mocker.patch("httpx.AsyncClient.post")
    mock_post.return_value.status_code = 500
    
    result = await fetch_vndb_novel_tags("1")
    
    assert result == []

@pytest.mark.asyncio
async def test_fetch_vndb_novel_tags_exception(mocker):
    mocker.patch("watchtower.CloudWatchLogHandler")
    
    mock_post = mocker.patch("httpx.AsyncClient.post")
    mock_post.side_effect = Exception("Test error")
    
    result = await fetch_vndb_novel_tags("1")
    
    assert result == []


def test_fetch_vndb_tags_description_success(mocker):
    mocker.patch("watchtower.CloudWatchLogHandler")
    
    mock_response = {
        "results": [{
            "id": "g32",
            "description": "Test description"
        }]
    }
    
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = mock_response
    
    result = fetch_vndb_tags_description("g32")
    
    assert result == "Test description"
    mock_post.assert_called_once()
    
    call_args = mock_post.call_args[1]
    assert "json" in call_args
    assert call_args["json"]["filters"] == ["id", "=", "g32"]
    assert call_args["json"]["fields"] == "description"

def test_fetch_vndb_tags_description_api_error(mocker):
    mocker.patch("watchtower.CloudWatchLogHandler")
    
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 500
    mock_post.return_value.text = "Internal Server Error"
    
    result = fetch_vndb_tags_description("g32")
    
    assert result is None
    mock_post.assert_called_once()

def test_fetch_vndb_tags_description_no_results(mocker):
    mocker.patch("watchtower.CloudWatchLogHandler")
    
    mock_response = {
        "results": []
    }
    
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = mock_response
    
    result = fetch_vndb_tags_description("g32")
    
    assert result is None
    mock_post.assert_called_once()

    