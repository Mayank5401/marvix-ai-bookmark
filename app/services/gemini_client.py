'''
import os
from langchain_google_genai import ChatGoogleGenerativeAI

GEMINI_API_KEY = "AIzaSyBbUYBh2uUxgWpfH-E7oXYJz_mi856saVc"

def get_gemini_llm():

    return ChatGoogleGenerativeAI(
        model="gemini-1.0-pro",
        temperature=0.3,
        google_api_key= GEMINI_API_KEY
    )
'''