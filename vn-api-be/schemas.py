from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class NovelsListResponse(BaseModel):
    id: int
    title: str
    status: str
    my_rating: int 
    tags: List["TagNovelResponce"] = []


class NovelsDetailResponse(BaseModel):
    id: int
    my_review: Optional[str] = None
    status: str
    language: str
    my_rating: Optional[int] = None
    vndb_id: str
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    studio: Optional[str] = None
    released: Optional[date] = None
    length: Optional[int] = None  # 1-5
    length_minutes: Optional[int] = None
    rating: Optional[float] = None
    votecount: Optional[int] = None
    user_rating: int
    tags: List["TagNovelResponce"] = []


class TagNovelResponce(BaseModel):
    id: int
    name: str


class NovelCreate(BaseModel):
    search_name: str  # ID новеллы на VNDB
    status: str = "reading"  # Статус: "reading", "completed" или другие
    my_review: Optional[str] = None  # Личный обзор
    my_rating: Optional[int] = None  # Личная оценка
    tags: List[str] = []


class TagCreate(BaseModel):
    id: int
    name: str
    description: str
    novels_id: Optional[List[int]] = []
