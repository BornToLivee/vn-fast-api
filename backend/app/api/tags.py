from typing import List

from app.core.logger import logger
from app.models.tag import Tag
from app.schemas.tag import TagList
from app.dependencies.database import db_dependency
from fastapi import APIRouter


router = APIRouter()


@router.get("/tags/", response_model=List[TagList] | str)
def tags_list(db: db_dependency):
    tags = db.query(Tag).all()
    if tags:
        logger.log("INFO", f"Found {len(tags)} tags")
        return tags

    logger.log("WARNING", "No tags found")
    return "No tags found yet"
