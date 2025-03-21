from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .models import Novel, SessionLocal, Tag
from .schemas import NovelCreate, NovelResponse

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/novels/", response_model=List[NovelResponse])
def read_novels(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    novels = db.query(Novel).offset(skip).limit(limit).all()
    return novels


@app.post("/novels/", response_model=NovelCreate)
def create_novel(novel: NovelCreate, db: Session = Depends(get_db)):
    db_novel = Novel(
        title=novel.title, 
        description=novel.description,
        my_rating=novel.my_rating
        )
    
    db.add(db_novel)
    db.commit()
    db.refresh(db_novel)

    if novel.tags_id:
        for tag_id in novel.tags_id:
            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag:
                db_novel.tags.append(tag)
            else:
                 raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")
            
        db.commit()
        db.refresh(db_novel)

    return db_novel
