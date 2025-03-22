import httpx
import requests

from app.schemas.novel import NovelSearchResponse
from app.core.logger import logger
from app.core.config import VNDB_API_URL


async def search_vndb_novels_by_name(query: str):
    json_payload = {
        "filters": ["search", "=", query],
        "fields": "id, title, image.url"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{VNDB_API_URL}/vn", json=json_payload)
        
        if response.status_code == 200:
            novels = response.json()["results"]
            result = []
            for novel in novels:
                result.append(NovelSearchResponse(
                    id=novel["id"],
                    title=novel["title"],
                    image_url=novel.get("image", {}).get("url", "")
                ))

            logger.log("INFO", f"Found {len(result)} novels for query: {query}")
            return result   

        else:
            logger.log("ERROR", f"Error searching for novels: {response.status_code} - {response.text}")
            return []
    

def fetch_vndb_novel(novel_id: str):
    json_payload = {
        "filters": ["id", "=", novel_id],
        "fields": "id, title, released, image.url, length, length_minutes, description, rating, votecount, developers.name"
    }
    
    logger.log("INFO", f"Fetching novel with ID: {novel_id}")
    
    response = requests.post(f"{VNDB_API_URL}/vn", json=json_payload)
    
    if response.status_code != 200:
        logger.log("ERROR", f"Failed to fetch novel: {response.status_code} - {response.text}")
        return None
    
    data = response.json()

    if "results" not in data:
        logger.log("WARNING", f"No results found for novel ID: {novel_id}")
        return None
    
    logger.log("INFO", f"Successfully fetched novel: {data['results'][0]['title']} with ID: {novel_id}")
    return data["results"][0]