from typing import List

from app.core.logger import logger
from app.schemas.tag import TagList
from app.dependencies.database import db_dependency
from app.dependencies.services import tag_service_dependency
from fastapi import APIRouter


router = APIRouter()


@router.get("/tags/", response_model=List[TagList] | str)
def tags_list(db: db_dependency, tag_service: tag_service_dependency):
    tags = tag_service.get_tags_list()
    return tags
