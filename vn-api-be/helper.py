import httpx

from schemas import NovelSearchResponse

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