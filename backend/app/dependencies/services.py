from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.settings import get_db

from app.services.tag import TagService
from app.services.vndb import VNDBService
from app.services.novel import NovelService
from app.repositories.novels import NovelRepository
from app.repositories.tags import TagRepository


def get_tag_repo(db: Session = Depends(get_db)):
    return TagRepository(db=db)


def get_tag_service(db: Session = Depends(get_db), repo=Depends(get_tag_repo)):
    return TagService(db=db, repo=repo)


def get_vndb_service(db: Session = Depends(get_db)):
    return VNDBService(db=db)


def get_novel_repo(db: Session = Depends(get_db)):
    return NovelRepository(db=db)


def get_novel_service(
    db: Session = Depends(get_db),
    vndb_service: VNDBService = Depends(get_vndb_service),
    tag_service: TagService = Depends(get_tag_service),
    repo: NovelRepository = Depends(get_novel_repo),
):
    return NovelService(
        db=db, repo=repo, vndb_service=vndb_service, tag_service=tag_service
    )


novel_service_dependency = Annotated[NovelService, Depends(get_novel_service)]
novel_repo_dependency = Annotated[NovelRepository, Depends(get_novel_repo)]

vndb_service_dependency = Annotated[VNDBService, Depends(get_vndb_service)]

tag_repo_dependency = Annotated[TagRepository, Depends(get_tag_repo)]
tag_service_dependency = Annotated[TagService, Depends(get_tag_service)]
