from sqlalchemy.orm import Session
from app.models.novel import Novel
from app.core.logger import logger
from fastapi import HTTPException
from app.schemas.novel import NovelCreate
from datetime import datetime


class NovelService:
    def __init__(self, db: Session, repo, vndb_service=None, tag_service=None):
        self.db = db
        self.repo = repo
        self.vndb_service = vndb_service
        self.tag_service = tag_service

    def get_novels_list(self):
        try:
            novels = self.repo.get_novels_list()
        except Exception as e:
            logger.log_exception("Error getting novels list", e)

        if not novels:
            logger.log("WARNING", "No novels found")
            return "No novels found"

        return novels

    def get_novel_by_id(self, novel_id: int):
        novel = self.repo.get_novel_by_id(novel_id)
        if not novel:
            logger.log_exception(
                f"Novel with id {novel_id} not found", Exception("Novel not found")
            )
            raise HTTPException(status_code=404, detail="Novel not found")

        return novel

    async def create_novel(self, novel_data: NovelCreate, vndb_id: str):
        existing_novel = self.repo.get_novel_by_vndb_id(vndb_id)
        if existing_novel:
            logger.log("INFO", f"Novel with vndb_id {vndb_id} already exists")
            raise HTTPException(status_code=400, detail="Novel already exists")

        novel_info = self.vndb_service.fetch_novel(vndb_id)
        if not novel_info:
            logger.log_exception(f"Novel details not found for vndb_id {vndb_id}")
            raise HTTPException(status_code=404, detail="Novel details not found")

        tag_data = await self.vndb_service.fetch_novel_tags(vndb_id)
        if not tag_data:
            logger.log("WARNING", f"Novel tags not found for vndb_id {vndb_id}")

        novel_tags = self.tag_service.create_or_get_tags(tag_data)

        new_novel = Novel(
            vndb_id=novel_info["id"],
            title=novel_info["title"],
            description=novel_info.get("description"),
            image_url=novel_info["image"]["url"] if "image" in novel_info else None,
            studio=(
                novel_info["developers"][0]["name"]
                if novel_info.get("developers")
                else None
            ),
            released=(
                datetime.strptime(novel_info["released"], "%Y-%m-%d").date()
                if novel_info.get("released")
                else None
            ),
            length=novel_info.get("length"),
            length_minutes=novel_info.get("length_minutes"),
            user_rating=novel_info.get("rating"),
            votecount=novel_info.get("votecount"),
            status=novel_data.status,
            my_review=novel_data.my_review,
            my_rating=novel_data.my_rating,
            language=novel_data.language,
        )

        # Add tags to the novel
        new_novel.tags = novel_tags

        self.repo.add(new_novel)

        return new_novel
