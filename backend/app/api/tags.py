from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.logger import logger
from app.database.settings import get_db
from app.models.tag import Tag
from app.schemas.tag import TagList
from typing import List

router = APIRouter()


@router.get("/tags/", response_model=List[TagList] | str)
def tags_list(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    if tags:
        logger.log("INFO", f"Found {len(tags)} tags")
        return tags

    logger.log("WARNING", "No tags found")
    return "No tags found yet"