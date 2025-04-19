import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from app.services.novel import NovelService
from app.schemas.novel import NovelCreate


class TestGetNovelsList:
    def test_returns_novels(self):
        mock_repo = MagicMock()
        mock_repo.get_novels_list.return_value = ["novel1", "novel2"]

        service = NovelService(db=None, repo=mock_repo)
        result = service.get_novels_list()

        assert result == ["novel1", "novel2"]
        mock_repo.get_novels_list.assert_called_once()

    def test_returns_warning_if_empty(self, mocker):
        mock_repo = MagicMock()
        mock_repo.get_novels_list.return_value = []

        mock_logger = mocker.patch("app.services.novel.logger")

        service = NovelService(db=None, repo=mock_repo)
        result = service.get_novels_list()

        assert result == "No novels found"
        mock_logger.log.assert_called_with("WARNING", "No novels found")


class TestGetNovelById:
    def test_returns_novel(self):
        mock_repo = MagicMock()
        mock_repo.get_novel_by_id.return_value = {"id": 1, "title": "Test"}

        service = NovelService(db=None, repo=mock_repo)
        result = service.get_novel_by_id(1)

        assert result["title"] == "Test"

    def test_raises_if_not_found(self, mocker):
        mock_repo = MagicMock()
        mock_repo.get_novel_by_id.return_value = None
        mock_logger = mocker.patch("app.services.novel.logger")

        service = NovelService(db=None, repo=mock_repo)
        with pytest.raises(HTTPException) as exc:
            service.get_novel_by_id(999)

        assert exc.value.status_code == 404
        assert exc.value.detail == "Novel not found"
        mock_logger.log_exception.assert_called()


class TestCreateNovel:
    @pytest.mark.asyncio
    async def test_create_successful(self, mocker):
        mock_repo = MagicMock()
        mock_repo.get_novel_by_vndb_id.return_value = None

        mock_vndb = MagicMock()
        mock_vndb.fetch_novel = MagicMock(
            return_value={
                "id": "v123",
                "title": "VN Title",
                "description": "desc",
                "image": {"url": "http://image"},
                "released": "2023-01-01",
                "length": 5,
                "length_minutes": 300,
                "rating": 8.5,
                "votecount": 50,
                "developers": [{"name": "Dev"}],
            }
        )
        mock_vndb.fetch_novel_tags = AsyncMock(
            return_value=[{"vndb_id": "g1", "name": "Test", "description": "desc"}]
        )

        mock_tag = MagicMock()
        mock_tag.name = "TagObj"
        mock_tags = MagicMock()
        mock_tags.create_or_get_tags.return_value = [mock_tag]

        service = NovelService(
            db=None, repo=mock_repo, vndb_service=mock_vndb, tag_service=mock_tags
        )
        novel_data = NovelCreate(
            status="planned", my_review="cool", my_rating=9.0, language="EN"
        )

        novel = await service.create_novel(novel_data, "v123")

        assert novel.title == "VN Title"
        assert novel.tags == [mock_tag]
        mock_repo.add.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_raises_if_exists(self):
        mock_repo = MagicMock()
        mock_repo.get_novel_by_vndb_id.return_value = True

        service = NovelService(db=None, repo=mock_repo)
        novel_data = NovelCreate(
            status="done", my_review="nice", my_rating=8, language="EN"
        )

        with pytest.raises(HTTPException) as exc:
            await service.create_novel(novel_data, "v123")

        assert exc.value.status_code == 400
        assert exc.value.detail == "Novel already exists"

    @pytest.mark.asyncio
    async def test_create_raises_if_novel_not_found(self, mocker):
        mock_repo = MagicMock()
        mock_repo.get_novel_by_vndb_id.return_value = None

        mock_vndb = MagicMock()
        mock_vndb.fetch_novel = MagicMock(return_value=None)

        mock_logger = mocker.patch("app.services.novel.logger")

        service = NovelService(db=None, repo=mock_repo, vndb_service=mock_vndb)
        novel_data = NovelCreate(
            status="done", my_review="nice", my_rating=8, language="EN"
        )

        with pytest.raises(HTTPException) as exc:
            await service.create_novel(novel_data, "v123")

        assert exc.value.status_code == 404
        assert exc.value.detail == "Novel details not found"
        mock_logger.log_exception.assert_called()
