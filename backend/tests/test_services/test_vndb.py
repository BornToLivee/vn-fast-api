import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.services.vndb import VNDBService


class TestVNDBService:
    @pytest.mark.asyncio
    async def test_search_novels_by_name(self, mocker):
        mock_response = {
            "results": [
                {
                    "id": "v123",
                    "title": "Anata no Osanazuma",
                    "image": {"url": "http://image1"},
                },
                {"id": "v124", "title": "VN Title", "image": {"url": "http://image2"}},
            ]
        }

        mock_post = mocker.patch("httpx.AsyncClient.post", new_callable=AsyncMock)
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = lambda: mock_response

        service = VNDBService(db=None)
        novels = await service.search_novels_by_name("VN Title")

        assert len(novels) == 2
        assert novels[0].id == "v123"
        assert novels[0].title == "Anata no Osanazuma"
        assert novels[0].image_url == "http://image1"
        assert novels[1].id == "v124"
        assert novels[1].title == "VN Title"
        assert novels[1].image_url == "http://image2"

    def test_fetch_novel(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "id": "v123",
                    "title": "Anata no Osanazuma",
                    "released": "2023-01-01",
                    "image": {"url": "http://image"},
                    "length": 5,
                    "length_minutes": 300,
                    "description": "This is a description",
                    "rating": 8.5,
                    "votecount": 50,
                    "developers": [{"name": "Dev"}],
                }
            ]
        }

        with patch("requests.post", return_value=mock_response):
            service = VNDBService(db=None)
            novel = service.fetch_novel("v123")

            assert novel["id"] == "v123"
            assert novel["title"] == "Anata no Osanazuma"

    @pytest.mark.asyncio
    async def test_fetch_vndb_novel_tags(self, mocker):
        mock_response = {
            "results": [
                {
                    "id": "v1",
                    "tags": [
                        {
                            "id": "g32",
                            "name": "ADV",
                            "category": "tech",
                            "rating": 2.764706,
                            "spoiler": 0,
                        },
                        {
                            "id": "g133",
                            "name": "Male Protagonist",
                            "category": "cont",
                            "rating": 2.9375,
                            "spoiler": 0,
                        },
                        {
                            "id": "g236",
                            "name": "Low Sexual Content",
                            "category": "ero",
                            "rating": 2.5555556,
                            "spoiler": 0,
                        },
                        {
                            "id": "g160",
                            "name": "Bloody Scenes",
                            "category": "cont",
                            "rating": 1.4,
                            "spoiler": 2,
                        },
                        {
                            "id": "g176",
                            "name": "Foolish Friend",
                            "category": "cont",
                            "rating": 0.21428572,
                            "spoiler": 0,
                        },
                    ],
                }
            ]
        }

        mock_response_obj = mocker.patch(
            "httpx.AsyncClient.post", new_callable=AsyncMock
        )
        mock_response_obj.return_value.status_code = 200
        mock_response_obj.return_value.json = lambda: mock_response

        mock_fetch = mocker.patch.object(
            VNDBService,
            "fetch_tag_description",
            side_effect=lambda x: "Test description",
        )

        service = VNDBService(db=None)
        result = await service.fetch_novel_tags("v1")

        assert len(result) == 2
        assert result[0]["vndb_id"] == "g32"
        assert result[0]["name"] == "ADV"
        assert result[0]["description"] == "Test description"

        assert result[1]["vndb_id"] == "g133"
        assert result[1]["name"] == "Male Protagonist"
        assert result[1]["description"] == "Test description"

        mock_response_obj.assert_called_once()
        mock_fetch.assert_has_calls([mocker.call("g32"), mocker.call("g133")])

        call_args = mock_response_obj.call_args[1]
        assert "json" in call_args
        assert call_args["json"]["filters"] == ["id", "=", "v1"]
        assert (
            call_args["json"]["fields"]
            == "tags.rating, tags.name, tags.category, tags.spoiler"
        )

    def test_fetch_tag_description(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{"description": "Action tag description"}]
        }

        with patch("requests.post", return_value=mock_response):
            service = VNDBService(db=None)
            description = service.fetch_tag_description("t123")

            assert description == "Action tag description"
