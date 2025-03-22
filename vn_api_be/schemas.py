from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class NovelSearchResponse(BaseModel):
    id: str
    title: str
    image_url: str

 
class NovelsListResponse(BaseModel):
    id: int
    title: str
    status: str
    my_rating: int 
    tags: List["TagNovelResponce"] = []


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
    tags: List["TagNovelResponce"] = []


class TagNovelResponce(BaseModel):
    id: int
    name: str


class NovelCreate(BaseModel):
    status: str = "reading"  # Статус: "reading", "completed" или другие
    my_review: Optional[str] = None  # Личный обзор
    my_rating: Optional[int] = None  # Личная оценка
    language: str = "russian"
    tags: List[str] = []


class TagCreate(BaseModel):
    id: int
    name: str
    description: str
    novels_id: Optional[List[int]] = []
