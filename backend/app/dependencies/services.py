from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.settings import get_db

from app.services.tag import TagService



def get_tag_service(db: Session = Depends(get_db)):
    return TagService(db=db, repo=None)

tag_service_dependency = Annotated[TagService, Depends(get_tag_service)]
