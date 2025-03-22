import pytest
from backend.app.models.novel import Novel

def test_novel_model():
    novel = Novel(
        vndb_id="123",
        title="Test Novel",
        description="This is a test novel",
        image_url="https://example.com/image.jpg",
        studio="Test Studio",
        released="2021-01-01",
        length=3,
        length_minutes=100,
        votecount=100,
        user_rating=5,
        tags = []
    )

    assert novel.vndb_id == "123"
    assert novel.title == "Test Novel"
    assert novel.description == "This is a test novel"
    assert novel.image_url == "https://example.com/image.jpg"
    assert novel.studio == "Test Studio"
    assert novel.released == "2021-01-01"
    assert novel.length == 3
    assert novel.length_minutes == 100
    assert novel.votecount == 100
    assert novel.user_rating == 5