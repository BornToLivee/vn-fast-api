from typing import List
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .models import Novel, SessionLocal, Tag
from .schemas import NovelCreate, NovelSearchResponse, TagCreate, NovelsListResponse, NovelsDetailResponse
from .helper import search_vndb_novels_by_name, fetch_vndb_novel

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/novels/search", response_model=List[NovelSearchResponse])
async def novel_search(query: str):
    novels = await search_vndb_novels_by_name(query)
    return novels


@app.get("/novels/", response_model=List[NovelsListResponse])
def read_novels(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    novels = db.query(Novel).offset(skip).limit(limit).all()
    return novels


@app.post("/novels/", response_model=NovelsDetailResponse)
def create_novel(vndb_id: str, novel_data: NovelCreate, db: Session = Depends(get_db)):
    # Проверяем, есть ли новелла уже в базе
    existing_novel = db.query(Novel).filter(Novel.vndb_id == vndb_id).first()
    if existing_novel:
        raise HTTPException(status_code=400, detail="Novel already exists")

    # Запрашиваем данные по VNDB ID
    novel_info = fetch_vndb_novel(vndb_id)
    if not novel_info:
        raise HTTPException(status_code=404, detail="Novel details not found")

    # Создаем объект новеллы
    new_novel = Novel(
        vndb_id=novel_info["id"],
        title=novel_info["title"],
        description=novel_info.get("description"),
        image_url=novel_info["image"]["url"] if "image" in novel_info else None,
        studio=novel_info["developers"][0]["name"] if novel_info.get("developers") else None,
        released=datetime.strptime(novel_info["released"], "%Y-%m-%d").date() if novel_info.get("released") else None,
        length=novel_info.get("length"),
        length_minutes=novel_info.get("length_minutes"),
        user_rating=novel_info.get("rating"),
        votecount=novel_info.get("votecount"),

        status=novel_data.status,
        my_review=novel_data.my_review,
        my_rating=novel_data.my_rating,
        language=novel_data.language
    )

    # Добавляем теги
    tags = []
    for tag_name in novel_data.tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
        tags.append(tag)

    new_novel.tags = tags

    db.add(new_novel)
    db.commit()
    db.refresh(new_novel)

    return new_novel