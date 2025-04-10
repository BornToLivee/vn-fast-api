from sqlalchemy.orm import Session

from app.models.tag import Tag
from app.core.logger import logger


def create_or_get_tags(tag_data: list, db: Session) -> list[Tag]:
    """
    Create or get existing tags from the database using bulk operations.

    :param tag_data: List of dictionaries with tag information
    :param db: Database session
    :return: List of Tag objects
    """
    tag_names = [tag["name"] for tag in tag_data]

    existing_tags = db.query(Tag).filter(Tag.name.in_(tag_names)).all()
    existing_tag_names = {tag.name: tag for tag in existing_tags}

    new_tags = []
    for tag_info in tag_data:
        if tag_info["name"] not in existing_tag_names:
            new_tag = Tag(
                name=tag_info["name"],
                description=tag_info["description"],
                vndb_id=tag_info["vndb_id"],
            )
            db.add(new_tag)
            new_tags.append(new_tag)

    if new_tags:
        db.commit()
        for tag in new_tags:
            db.refresh(tag)

    all_tags = list(existing_tags) + new_tags

    logger.log("INFO", f"Total tags processed: {len(all_tags)}")
    return all_tags
