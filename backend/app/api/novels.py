from datetime import datetime
from typing import List

from app.core.logger import logger
from app.database.settings import get_db
from app.models.novel import Novel
from app.schemas.novel import (
    NovelCreate,
    NovelsDetailResponse,
    NovelSearchResponse,
    NovelsListResponse,
)
from app.services.tag import create_or_get_tags
from app.services.vndb import (
    fetch_vndb_novel,
    fetch_vndb_novel_tags,
    search_vndb_novels_by_name,
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

router = APIRouter()


@router.delete("/novels/delete")
def clear_database(db: Session = Depends(get_db)):
    """
    Clear all novels and their related data from the database.
    This will delete all records from novels and novel_tag tables.
    """
    try:
        # First delete all records from the novel_tag table
        db.execute(text("DELETE FROM novel_tag"))
        # Then delete all records from the novels and tag table
        db.execute(text("DELETE FROM novels"))
        db.execute(text("DELETE FROM tags"))
        db.commit()
        logger.log("INFO", "All novels and related data have been cleared")
        return {"message": "All novels and related data have been cleared"}
    except Exception as e:
        db.rollback()
        logger.log_exception("Error clearing database", e)
        raise HTTPException(status_code=500, detail="Error clearing database")


@router.get("/novels/search", response_model=List[NovelSearchResponse])
async def novel_search(query: str):
    logger.log("INFO", f"Search query: {query}")
    novels = await search_vndb_novels_by_name(query)
    return novels


@router.get("/novels/", response_model=List[NovelsListResponse] | str)
def read_novels(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    novels = db.query(Novel).offset(skip).limit(limit).all()

    if not novels:
        logger.log("WARNING", "No novels found")
        return "No novels found yet"

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
async def create_novel(
    vndb_id: str, novel_data: NovelCreate, db: Session = Depends(get_db)
):
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
    """

    existing_novel = db.query(Novel).filter(Novel.vndb_id == vndb_id).first()
    if existing_novel:
        logger.log("INFO", f"Novel with vndb_id {vndb_id} already exists")
        raise HTTPException(status_code=400, detail="Novel already exists")

    novel_info = fetch_vndb_novel(vndb_id)
    if not novel_info:
        logger.log("ERROR", f"Novel details not found for vndb_id {vndb_id}")
        raise HTTPException(status_code=404, detail="Novel details not found")

    tag_data = await fetch_vndb_novel_tags(vndb_id)
    if not tag_data:
        logger.log("WARNING", f"Novel tags not found for vndb_id {vndb_id}")

    novel_tags = create_or_get_tags(tag_data, db)

    new_novel = Novel(
        vndb_id=novel_info["id"],
        title=novel_info["title"],
        description=novel_info.get("description"),
        image_url=novel_info["image"]["url"] if "image" in novel_info else None,
        studio=(
            novel_info["developers"][0]["name"]
            if novel_info.get("developers")
            else None
        ),
        released=(
            datetime.strptime(novel_info["released"], "%Y-%m-%d").date()
            if novel_info.get("released")
            else None
        ),
        length=novel_info.get("length"),
        length_minutes=novel_info.get("length_minutes"),
        user_rating=novel_info.get("rating"),
        votecount=novel_info.get("votecount"),
        status=novel_data.status,
        my_review=novel_data.my_review,
        my_rating=novel_data.my_rating,
        language=novel_data.language,
    )

    # Add tags to the novel
    new_novel.tags = novel_tags

    db.add(new_novel)
    db.commit()
    db.refresh(new_novel)

    return new_novel
