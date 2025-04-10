from app.models.tag import Tag

def test_read_tags(client, db):
    tag1 = Tag(
        name="Test Tag 1", 
        description="This is a test tag 1", 
        vndb_id="g1"
    )
    tag2 = Tag(
        name="Test Tag 2", 
        description="This is a test tag 2", 
        vndb_id="g2"
    )

    db.add(tag1)
    db.add(tag2)
    db.commit()

    response = client.get("/tags/")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == "Test Tag 1"
    assert data[0]["description"] == "This is a test tag 1"
    assert data[0]["vndb_id"] == "g1"
    assert data[1]["name"] == "Test Tag 2"
    assert data[1]["description"] == "This is a test tag 2"
    assert data[1]["vndb_id"] == "g2"
    assert len(data) == 2
