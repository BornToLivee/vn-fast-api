from app.models.novel import Novel
from app.repositories.base import BaseRepository


class NovelRepository(BaseRepository):
    def __init__(self, db):
        self.db = db

    def add(self, novel: Novel) -> Novel:
        self.db.add(novel)
        self.db.commit()
        self.db.refresh(novel)
        return novel
    
    def get_novels_list(self):
        return self.db.query(Novel).all()
    
    def get_novel_by_id(self, novel_id: int):
        return self.db.query(Novel).filter(Novel.id == novel_id).first()
    
    def get_novel_by_vndb_id(self, vndb_id: str):
        return self.db.query(Novel).filter(Novel.vndb_id == vndb_id).first()
    