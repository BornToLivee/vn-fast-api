from typing import List

from app.core.logger import logger
from app.dependencies.database import db_dependency
from app.dependencies.services import novel_service_dependency, vndb_service_dependency
from app.schemas.novel import (
    NovelCreate,
    NovelsDetailResponse,
    NovelSearchResponse,
    NovelsListResponse,
)
from fastapi import APIRouter, HTTPException
from sqlalchemy import text

router = APIRouter()


@router.delete("/novels/delete")
def clear_database(db: db_dependency):
    """
    Clear all novels and their related data from the database.
    This will delete all records from novels, tags and novel_tag tables.
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
async def novel_search(query: str, vndb_service: vndb_service_dependency):
    logger.log("INFO", f"Search query: {query}")
    novels = await vndb_service.search_novels_by_name(query)
    return novels


@router.get("/novels/", response_model=List[NovelsListResponse] | str)
def read_novels(novel_service: novel_service_dependency):
    novels = novel_service.get_novels_list()
    logger.log("INFO", f"Found {len(novels)} novels" if novels else "No novels found")
    return novels


@router.get("/novels/{novel_id}", response_model=NovelsDetailResponse)
def read_novel(novel_id: int, novel_service: novel_service_dependency):
    novel = novel_service.get_novel_by_id(novel_id)
    return novel


@router.post("/novels/", response_model=NovelsDetailResponse)
async def create_novel(
    vndb_id: str, novel_data: NovelCreate, novel_service: novel_service_dependency
):
    new_novel = await novel_service.create_novel(novel_data, vndb_id)
    return new_novel
