class BaseRepository:
    def __init__(self, db):
        self.db = db

    def add(self, obj):
        self.db.add(obj)

    def commit(self):
        self.db.commit()

    def refresh(self, obj):
        self.db.refresh(obj)

    def delete(self, obj):
        self.db.delete(obj)
