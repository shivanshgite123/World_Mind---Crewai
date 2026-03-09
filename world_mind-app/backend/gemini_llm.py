import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
_model = genai.GenerativeModel("gemini-1.5-flash")

PROMPT_TEMPLATE = """
You are a professional news analyst. Use the following retrieved news context to answer the user's query.

Context:
{context}

Question:
{query}

Generate a concise, well-structured summary in 3-5 bullet points.
Each bullet point should start with • and cover a distinct key insight.
Be factual, clear, and informative. Do not add information not present in the context.
"""


def generate_summary(query: str, context: str) -> str:
    """Send context + query to Gemini and return bullet-point summary."""
    if not context.strip():
        return "• No relevant news articles were found for this query. Please try a different search term."

    prompt = PROMPT_TEMPLATE.format(query=query, context=context)
    response = _model.generate_content(prompt)
    return response.text.strip()
