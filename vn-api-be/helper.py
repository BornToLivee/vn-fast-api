import httpx
import requests

from .schemas import NovelSearchResponse

VNDB_API_URL = "https://api.vndb.org/kana"

async def search_vndb_novels_by_name(query: str):
    json_payload = {
        "filters": ["search", "=", query],
        "fields": "id, title, image.url"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{VNDB_API_URL}/vn", json=json_payload)
        
        if response.status_code == 200:
            return [
                NovelSearchResponse(
                    id=novel["id"],
                    title=novel["title"],
                    image_url=novel["image"]["url"] if "image" in novel else ""
                )
                for novel in response.json()["results"]
            ]
        return []
    

def fetch_vndb_novel(novel_id: str):
        json_payload = {
        "filters": ["id", "=", novel_id],
        "fields": "id, title, released, image.url, length, length_minutes, description, rating, votecount, developers.name"
    }
        
        response = requests.post(f"{VNDB_API_URL}/vn", json=json_payload)
            
        if response.status_code != 200:
            return None
        
        data = response.json()

        if "results" not in data:
            return None
        
        return data["results"][0]