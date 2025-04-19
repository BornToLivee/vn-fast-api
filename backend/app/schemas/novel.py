from datetime import date
from typing import List, Optional

from app.schemas.tag import TagNovelResponse
from pydantic import BaseModel


class NovelSearchResponse(BaseModel):
    id: str
    title: str
    image_url: str


class NovelsListResponse(BaseModel):
    id: int
    title: str
    status: str
    my_rating: float
    image_url: str


class NovelsDetailResponse(BaseModel):
    id: int
    vndb_id: str
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    studio: Optional[str] = None
    released: Optional[date] = None
    length: Optional[int] = None  # 1-5
    length_minutes: Optional[int] = None
    user_rating: Optional[float] = None
    votecount: Optional[int] = None

    my_review: Optional[str] = None
    status: str
    language: str
    my_rating: Optional[float] = None
    tags: List[TagNovelResponse] = []
    completed_date: Optional[date] = None


class NovelCreate(BaseModel):
    status: str = "READING"
    my_review: Optional[str] = None
    my_rating: Optional[float] = None
    language: str = "RUSSIAN"
    completed_date: Optional[date] = None
