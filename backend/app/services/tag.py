from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.core.logger import logger


def create_or_get_tags(tag_data: list, db: Session) -> list[Tag]:
    """
    Create or get existing tags from the database.
    
    :param tag_data: List of dictionaries with tag information
    :param db: Database session
    :return: List of Tag objects
    """
    tags = []
    for tag_info in tag_data:
        existing_tag = db.query(Tag).filter(Tag.name == tag_info["name"]).first()
        if existing_tag:
            logger.log("INFO", f"Tag '{tag_info['name']}' already exists in the database.")
            tags.append(existing_tag)
        else:
            new_tag = Tag(
                name=tag_info["name"],
                description=tag_info["description"],
                vndb_id=tag_info["vndb_id"],
            )
            db.add(new_tag)
            db.commit()
            db.refresh(new_tag)
            logger.log("INFO", f"Created new tag '{new_tag.name}' with ID '{new_tag.id}'.")
            tags.append(new_tag)
            
    logger.log("INFO", f"Total tags processed: {len(tags)}.")
    return tags