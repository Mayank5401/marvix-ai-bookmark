from fastapi import HTTPException
import httpx

WIKI_API_URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": "MarvixAI/1.0 (contact: mayank@example.com)"
}


async def search_wikipedia(query: str, limit: int = 5):
    try:
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": limit,
        }

        async with httpx.AsyncClient(timeout=10.0, headers=HEADERS) as client:
            response = await client.get(WIKI_API_URL, params=params)
            response.raise_for_status()
            data = response.json() 
          
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Wikipedia API unavailable")

    return [
        {
            "title": item["title"],
            "url": f"https://en.wikipedia.org/wiki/{item['title'].replace(' ', '_')}",
            "snippet": item["snippet"]
        }
        for item in data["query"]["search"]
    ]
