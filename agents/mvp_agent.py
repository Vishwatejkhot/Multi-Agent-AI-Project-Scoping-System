from langchain_groq import ChatGroq
from config import GROQ_API_KEY, MODEL_NAME
from pydantic import BaseModel, ValidationError
import json
import re


client = ChatGroq(
    api_key=GROQ_API_KEY,
    model=MODEL_NAME,
    temperature=0.3
)


class MVPOutput(BaseModel):
    core_features: list[str]
    optional_features: list[str]
    integrations: int
    ai_features: bool


SYSTEM_PROMPT = """
You are a Senior CTO.

Design a realistic MVP.
Avoid overbuilding.
Be practical and engineering-focused.

Return ONLY valid JSON.
Do NOT explain.
Do NOT use markdown.
"""


def clean_json(content: str):
    content = content.strip()

    # Remove ```json blocks if present
    if content.startswith("```"):
        content = re.sub(r"```.*?\n", "", content)
        content = content.replace("```", "")

    return content.strip()


def generate_mvp(idea: str, context: str):

    USER_PROMPT = f"""
Context:
{context}

Startup Idea:
{idea}

Return JSON:
{{
  "core_features": [],
  "optional_features": [],
  "integrations": 0,
  "ai_features": false
}}
"""

    response = client.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT}
    ])

    content = clean_json(response.content)

    try:
        parsed = json.loads(content)
        validated = MVPOutput(**parsed)
        return validated.dict()
    except (json.JSONDecodeError, ValidationError):
        return {
            "error": "MVP parsing failed",
            "raw_output": content
        }