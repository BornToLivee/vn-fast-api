from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.settings import get_db

from app.services.tag import TagService
from app.services.vndb import VNDBService
from app.services.novel import NovelService



def get_tag_service(db: Session = Depends(get_db)):
    return TagService(db=db, repo=None)

def get_vndb_service(db: Session = Depends(get_db)):
    return VNDBService(db=db)

def get_novel_service(db: Session = Depends(get_db), vndb_service: VNDBService = Depends(get_vndb_service), tag_service: TagService = Depends(get_tag_service)):
    return NovelService(db=db, repo=None, vndb_service=vndb_service, tag_service=tag_service)


novel_service_dependency = Annotated[NovelService, Depends(get_novel_service)]
vndb_service_dependency = Annotated[VNDBService, Depends(get_vndb_service)]
tag_service_dependency = Annotated[TagService, Depends(get_tag_service)]
