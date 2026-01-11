from .gemini_client import get_gemini_llm
from .prompt import TAG_PROMPT
import re
from collections import Counter

STOPWORDS = {
    "the", "and", "of", "to", "in", "a", "for", "with", "on", "by"
}

def parse_tags(text: str) -> list[str]:
    return [
        t.strip().lower()
        for t in text.split(",")
        if t.strip()
    ]
'''
async def generate_tags(title: str, url: str) -> list[str]:
    llm = get_gemini_llm()
    prompt = TAG_PROMPT.format(title=title, url=url)

    try:
        response = await llm.ainvoke(prompt)
        print("Gemini raw response:", response.content)
        return parse_tags(response.content)
    except Exception as e:
        print("Gemini error:", repr(e))
        return ["uncategorized"]
'''

def generate_tags(title: str, url: str) -> list[str]:
    text = f"{title} {url}".lower()
    words = re.findall(r"[a-z]{3,}", text)

    keywords = [
        w for w in words
        if w not in STOPWORDS
    ]

    most_common = Counter(keywords).most_common(5)
    return [word for word, _ in most_common]