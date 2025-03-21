from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .models import Novel, SessionLocal, Tag
from .schemas import NovelCreate, NovelResponse, TagCreate
from .helper import search_vndb_novels_by_name

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TODO ensuure correct query
@app.get("/novels/search", response_model=List[NovelResponse])
async def novel_search(query: str):
    novels = await search_vndb_novels_by_name(query)
    return novels


@app.get("/novels/", response_model=List[NovelResponse])
def read_novels(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    novels = db.query(Novel).offset(skip).limit(limit).all()
    return novels
