from typing import List, Optional

from pydantic import BaseModel


class TagNovelResponse(BaseModel):
    id: int
    name: str


class TagCreate(BaseModel):
    id: int
    name: str
    description: str
    novels_id: Optional[List[int]] = []


class TagList(BaseModel):
    id: int
    vndb_id: str
    name: str
    description: str
