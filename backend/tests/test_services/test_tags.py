from unittest.mock import MagicMock
from app.services.tag import TagService
from app.models.tag import Tag


class TestTagService:
    def test_get_tags_list(self):
        # Создаем мок репозитория
        mock_repo = MagicMock()
        mock_repo.get_tags_list.return_value = [
            Tag(name="Test Tag 1", description="Description 1", vndb_id="v1"),
            Tag(name="Test Tag 2", description="Description 2", vndb_id="v2"),
        ]

        # Инициализация сервиса
        service = TagService(db=None, repo=mock_repo)

        # Тестируем метод
        tags = service.get_tags_list()

        # Проверяем, что метод возвращает правильные данные
        assert len(tags) == 2
        assert tags[0].name == "Test Tag 1"
        assert tags[1].name == "Test Tag 2"
        mock_repo.get_tags_list.assert_called_once()

    def test_get_tags_list_empty(self):
        mock_repo = MagicMock()
        mock_repo.get_tags_list.return_value = []

        service = TagService(db=None, repo=mock_repo)

        result = service.get_tags_list()

        assert result == "No tags found"
        mock_repo.get_tags_list.assert_called_once()

    def test_create_or_get_tags(self):
        tag_data = [
            {"name": "New Tag", "description": "New Tag Desc", "vndb_id": "v123"},
            {
                "name": "Existing Tag",
                "description": "Existing Tag Desc",
                "vndb_id": "v456",
            },
        ]

        mock_repo = MagicMock()
        mock_repo.get_existing_tags.return_value = [
            Tag(name="Existing Tag", description="Existing Tag Desc", vndb_id="v456")
        ]
        mock_repo.add = MagicMock()
        mock_repo.commit = MagicMock()
        mock_repo.refresh = MagicMock()

        service = TagService(db=None, repo=mock_repo)

        tags = service.create_or_get_tags(tag_data)

        # Проверяем, что новая метка была добавлена
        assert len(tags) == 2
        assert tags[0].name == "Existing Tag"
        assert tags[1].name == "New Tag"
        mock_repo.add.assert_called_once_with(
            tags[1]
        )  # Проверка, что новая метка была добавлена
        mock_repo.commit.assert_called_once()
        mock_repo.refresh.assert_called()

    def test_create_or_get_tags_no_new_tags(self):
        tag_data = [
            {
                "name": "Existing Tag",
                "description": "Existing Tag Desc",
                "vndb_id": "v456",
            },
        ]

        mock_repo = MagicMock()
        mock_repo.get_existing_tags.return_value = [
            Tag(name="Existing Tag", description="Existing Tag Desc", vndb_id="v456")
        ]

        service = TagService(db=None, repo=mock_repo)

        tags = service.create_or_get_tags(tag_data)

        # Проверяем, что никаких новых тегов не добавлено
        assert len(tags) == 1
        assert tags[0].name == "Existing Tag"
        mock_repo.add.assert_not_called()
        mock_repo.commit.assert_not_called()
        mock_repo.refresh.assert_not_called()
