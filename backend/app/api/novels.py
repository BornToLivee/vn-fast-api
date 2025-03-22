from typing import List
from datetime import datetime

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.models.novel import Novel
from app.models.tag import Tag
from app.schemas.novel import NovelCreate, NovelSearchResponse, NovelsListResponse, NovelsDetailResponse
from app.services.vndb import search_vndb_novels_by_name, fetch_vndb_novel
from app.core.logger import logger
from app.database.settings import get_db

router = APIRouter()

@router.get("/novels/search", response_model=List[NovelSearchResponse])
async def novel_search(query: str):
    logger.log("INFO", f"Search query: {query}")
    novels = await search_vndb_novels_by_name(query)
    return novels


@router.get("/novels/", response_model=List[NovelsListResponse])
def read_novels(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    novels = db.query(Novel).offset(skip).limit(limit).all()

    if not novels:
        logger.log("WARNING", "No novels found")
        return []

    logger.log("INFO", f"Found {len(novels)} novels")
    return novels


@router.get("/novels/{novel_id}", response_model=NovelsDetailResponse)
def read_novel(novel_id: int, db: Session = Depends(get_db)):
    novel = db.query(Novel).filter(Novel.id == novel_id).first()
    if not novel:
        logger.log("ERROR", f"Novel with id {novel_id} not found")
        raise HTTPException(status_code=404, detail="Novel not found")
    
    return novel


@router.post("/novels/", response_model=NovelsDetailResponse)
def create_novel(vndb_id: str, novel_data: NovelCreate, db: Session = Depends(get_db)):
    
    """
    Create a new novel entry in the database using the provided VNDB ID and novel data.

    This function checks if a novel with the given VNDB ID already exists in the database.
    If it exists, it raises an HTTP 400 error. Otherwise, it fetches the novel details
    from VNDB, creates a new novel entry with the provided and fetched details, and adds
    it to the database. If the VNDB details cannot be fetched, an HTTP 404 error is raised.

    :param vndb_id: The VNDB ID of the novel to be created.
    :param novel_data: The data required to create the novel, including status, review, 
                       rating, language, and tags.
    :param db: The database session dependency for performing database operations.
    
    :return: The newly created novel with its details.
    :raises HTTPException: If the novel already exists or if VNDB details cannot be fetched.
    """

    existing_novel = db.query(Novel).filter(Novel.vndb_id == vndb_id).first()
    if existing_novel:
        logger.log("INFO", f"Novel with vndb_id {vndb_id} already exists")
        raise HTTPException(status_code=400, detail="Novel already exists")

    novel_info = fetch_vndb_novel(vndb_id)
    if not novel_info:
        logger.log("ERROR", f"Novel details not found for vndb_id {vndb_id}")
        raise HTTPException(status_code=404, detail="Novel details not found")


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

    tags = []

    for tag_name in novel_data.tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if tag:
            tags.append(tag)

    logger.log("INFO", f"Tags: {tags}")
    new_novel.tags = tags

    db.add(new_novel)
    db.commit()
    db.refresh(new_novel)

    return new_novel