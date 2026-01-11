TAG_PROMPT = """
You are a system that generates category tags.

Given a Wikipedia article title and URL,
return 3 to 5 concise category tags.

Rules:
- Use lowercase
- Single words only
- No explanations
- Output as comma-separated values

Title: {title}
URL: {url}
"""
