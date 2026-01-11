import httpx
import re

WIKI_API_URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": "MarvixAI/1.0 (contact: user@example.com)"
}
STOP_PHRASES = [
    "at the",
    "from",
    "of",
    "in",
    "by",
]

GENERIC_REPLACEMENTS = {
    "cricketers": "cricket",
    "players": "sports",
    "athletes": "sports",
    "activists": "activism",
    "politicians": "politics",
    "philosophers": "philosophy",
    "scientists": "science",
    "writers": "literature",
    "actors": "film",
    "singers": "music",
}

def normalize_category(cat: str) -> str:
    cat = cat.lower()

    # remove years
    cat = re.sub(r"\b\d{4}\b", "", cat)

    # cut at stop phrases
    for phrase in STOP_PHRASES:
        if phrase in cat:
            cat = cat.split(phrase)[0]

    cat = cat.strip()

    # replace plural roles with domains
    for key, value in GENERIC_REPLACEMENTS.items():
        if key in cat:
            return value

    # fallback: last meaningful word
    words = cat.split()
    return words[-1] if words else cat

def clean_categories(categories: list[str]) -> list[str]:
    cleaned = []

    for cat in categories:
        cat = cat.lower()

        # drop pure year-based categories
        if re.fullmatch(r"\d{4} (births|deaths)", cat):
            continue

        # drop centuries
        if "century" in cat:
            continue

        # drop wikipedia maintenance categories
        if "wikipedia" in cat or "articles" in cat:
            continue

        cleaned.append(cat)

    normalized = list(
    dict.fromkeys(normalize_category(c) for c in cleaned)
    )

    return normalized[:5]


async def get_wikipedia_categories(title: str, limit: int = 5) -> list[str]:
    params = {
    "action": "query",
    "prop": "categories",
    "titles": title,
    "format": "json",
    "cllimit": "max",       
    "clshow": "!hidden",     
    "redirects": 1          
    }


    async with httpx.AsyncClient(headers=HEADERS, timeout=10) as client:
        response = await client.get(WIKI_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

    pages = data["query"]["pages"]
    page = next(iter(pages.values()))

    categories = page.get("categories", [])

    raw = [
        cat["title"].replace("Category:", "").strip().lower()
        for cat in categories
    ]

    # print("RAW WIKI CATEGORIES:", raw)

    cleaned = clean_categories(raw)
    return cleaned[:limit]


    
