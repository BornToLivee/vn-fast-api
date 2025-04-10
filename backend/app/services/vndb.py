import httpx
import requests


from app.schemas.novel import NovelSearchResponse
from app.core.logger import logger
from app.core.config import (
    ACCEPTABLE_TAGS_IMPORTANCE_RATING as ATIR,
    ACCEPTABLE_TAGS_SPOILER_VALUE as ATSV,
    VNDB_API_URL,
)


async def search_vndb_novels_by_name(query: str):
    json_payload = {"filters": ["search", "=", query], "fields": "id, title, image.url"}

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{VNDB_API_URL}/vn", json=json_payload)
        if response.status_code == 200:
            novels = response.json()["results"]
            result = []
            for novel in novels:
                result.append(
                    NovelSearchResponse(
                        id=novel["id"],
                        title=novel["title"],
                        image_url=novel.get("image", {}).get("url", ""),
                    )
                )

            logger.log("INFO", f"Found {len(result)} novels for query: {query}")
            return result

        else:
            logger.log(
                "ERROR",
                f"Error searching for novels: {response.status_code} - {response.text}",
            )
            return []


def fetch_vndb_novel(novel_id: str):
    json_payload = {
        "filters": ["id", "=", novel_id],
        "fields": "id, title, released, image.url, length, length_minutes, description, rating, votecount, developers.name",
    }

    logger.log("INFO", f"Fetching novel with ID: {novel_id}")

    response = requests.post(f"{VNDB_API_URL}/vn", json=json_payload)

    if response.status_code != 200:
        logger.log(
            "ERROR", f"Failed to fetch novel: {response.status_code} - {response.text}"
        )
        return None

    data = response.json()

    if "results" not in data:
        logger.log("WARNING", f"No results found for novel ID: {novel_id}")
        return None

    logger.log(
        "INFO",
        f"Successfully fetched novel: {data['results'][0]['title']} with ID: {novel_id}",
    )
    return data["results"][0]


async def fetch_vndb_novel_tags(novel_id: str):
    """
    Fetch tags for a novel from VNDB API.

    :param novel_id: VNDB ID of the novel
    :return: List of dictionaries with tag information
    """
    filtered_tags = []
    json_payload = {
        "filters": ["id", "=", novel_id],
        "fields": "tags.rating, tags.name, tags.category, tags.spoiler",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{VNDB_API_URL}/vn", json=json_payload)

            if response.status_code == 200:
                all_tags = response.json()["results"]

                logger.log("INFO", f"All tags: {all_tags}")
                for tags in all_tags:
                    for tag in tags["tags"]:
                        if (
                            tag["category"] != "ero"
                            and tag["rating"] > ATIR
                            and tag["spoiler"] <= ATSV
                        ):
                            filtered_tags.append(
                                {
                                    "name": tag["name"],
                                    "description": fetch_vndb_tags_description(tag["id"]),
                                    "vndb_id": tag["id"],
                                }
                            )
                            logger.log("Info", f"Filtered tags: {filtered_tags}")
            else:
                logger.log(
                    "WARNING", f"Api error, impossible fetch tags for novel {novel_id}"
                )
                return []
        except Exception as e:
            logger.log(
                "WARNING",
                f"Unexpected error {e}, impossible fetch tags for novel {novel_id}",
            )
            return []

    return filtered_tags


def fetch_vndb_tags_description(tag_id: str):
    json_payload = {
        "filters": ["id", "=", tag_id],
        "fields": "description",
    }

    response = requests.post(f"{VNDB_API_URL}/tag", json=json_payload)

    if response.status_code != 200:
        logger.log(
            "ERROR", f"Failed to fetch tag description: {response.status_code} - {response.text}"
        )
        return None

    data = response.json()

    if "results" not in data:
        logger.log("WARNING", f"No results found for tag ID: {tag_id}")
        return None

    return data["results"][0]["description"]

