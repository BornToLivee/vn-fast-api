from pydantic import BaseModel
from typing import List, Optional


class NovelResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    my_rating: int 
    tags: List["TagNovelResponce"] = []


class TagNovelResponce(BaseModel):
    id: int
    name: str


class NovelCreate(BaseModel):
    id: int
    title: str
    description: Optional[str]
    my_rating: int 
    tags_id: Optional[List[int]] = []


class TagCreate(BaseModel):
    id: int
    name: str
    description: str
    novels_id: Optional[List[int]] = []
