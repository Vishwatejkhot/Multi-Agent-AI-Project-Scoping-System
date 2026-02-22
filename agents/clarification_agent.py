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


class ClarificationOutput(BaseModel):
    target_users: str
    platform: str
    revenue_model: str
    budget_range: str
    timeline_expectation: str
    assumptions: list[str]


SYSTEM_PROMPT = """
You are a Senior Product Strategist.

Your job is to clarify startup ideas before scoping.

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


def generate_clarifications(idea: str):

    USER_PROMPT = f"""
Startup Idea:
{idea}

Extract or infer:

1. Target users
2. Platform (Web, Mobile, Both)
3. Revenue model
4. Budget range
5. Timeline expectation
6. List assumptions if information is missing

Return JSON:
{{
  "target_users": "",
  "platform": "",
  "revenue_model": "",
  "budget_range": "",
  "timeline_expectation": "",
  "assumptions": []
}}
"""

    response = client.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT}
    ])

    content = clean_json(response.content)

    try:
        parsed = json.loads(content)
        validated = ClarificationOutput(**parsed)
        return validated.dict()
    except (json.JSONDecodeError, ValidationError):
        return {
            "error": "Clarification parsing failed",
            "raw_output": content
        }