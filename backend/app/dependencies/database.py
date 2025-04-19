from typing import Annotated

from app.database.settings import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

db_dependency = Annotated[Session, Depends(get_db)]
