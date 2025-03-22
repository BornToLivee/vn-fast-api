from pydantic import BaseModel
from typing import List, Optional


class TagNovelResponse(BaseModel):
    id: int
    name: str


class TagCreate(BaseModel):
    id: int
    name: str
    description: str
    novels_id: Optional[List[int]] = []
