from app.core.logger import logger
from app.models.tag import Tag
from sqlalchemy.orm import Session


class TagService:
    def __init__(self, db: Session, repo):
        self.db = db
        self.repo = repo

    def get_tags_list(self):
        tags = self.repo.get_tags_list()

        if tags:
            logger.log("INFO", f"Found {len(tags)} tags")
            return tags
        else:
            logger.log("WARNING", "No tags found")
            return "No tags found"

    def create_or_get_tags(self, tag_data: list):
        """
        Create or get existing tags from the database using bulk operations.

        :param tag_data: List of dictionaries with tag information
        :param db: Database session
        :return: List of Tag objects
        """
        tag_names = [tag["name"] for tag in tag_data]

        existing_tags = self.repo.get_existing_tags(tag_names)
        existing_tag_names = {tag.name: tag for tag in existing_tags}

        new_tags = []
        for tag_info in tag_data:
            if tag_info["name"] not in existing_tag_names:
                new_tag = Tag(
                    name=tag_info["name"],
                    description=tag_info["description"],
                    vndb_id=tag_info["vndb_id"],
                )
                self.repo.add(new_tag)
                new_tags.append(new_tag)

        if new_tags:
            self.repo.commit()
            for tag in new_tags:
                self.repo.refresh(tag)

        all_tags = list(existing_tags) + new_tags

        logger.log("INFO", f"Total tags processed: {len(all_tags)}")
        return all_tags
