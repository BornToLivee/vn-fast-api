from app.models.tag import Tag


def test_read_tags(client, db):
    tag1 = Tag(name="Test Tag 1", description="This is a test tag 1", vndb_id="g1")
    tag2 = Tag(name="Test Tag 2", description="This is a test tag 2", vndb_id="g2")

    db.add_all([tag1, tag2])
    db.commit()

    response = client.get("/tags/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2

    expected = {
        "g1": {"name": "Test Tag 1", "description": "This is a test tag 1"},
        "g2": {"name": "Test Tag 2", "description": "This is a test tag 2"},
    }

    for tag in data:
        vndb_id = tag["vndb_id"]
        assert vndb_id in expected
        assert tag["name"] == expected[vndb_id]["name"]
        assert tag["description"] == expected[vndb_id]["description"]
