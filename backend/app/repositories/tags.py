from app.models.tag import Tag
from app.repositories.base import BaseRepository


class TagRepository(BaseRepository):
    def __init__(self, db):
        self.db = db

    def get_tags_list(self):
        return self.db.query(Tag).all()
    
    def get_existing_tags(self, tag_names: list):
        return self.db.query(Tag).filter(Tag.name.in_(tag_names)).all()
