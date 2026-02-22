from langchain_groq import ChatGroq
from config import GROQ_API_KEY, MODEL_NAME
from pydantic import BaseModel, ValidationError
import json
import re


client = ChatGroq(
    api_key=GROQ_API_KEY,
    model=MODEL_NAME,
    temperature=0.4
)


class RiskOutput(BaseModel):
    technical_risks: list[str]
    business_risks: list[str]


SYSTEM_PROMPT = """
You are a Senior CTO performing pre-investment risk analysis.

Be realistic.
Be conservative.
Return ONLY valid JSON.
Do NOT explain.
Do NOT use markdown.
"""


def clean_json(content: str):
    content = content.strip()

    if content.startswith("```"):
        content = re.sub(r"```.*?\n", "", content)
        content = content.replace("```", "")

    return content.strip()


def generate_risks(idea: str):

    USER_PROMPT = f"""
Startup Idea:
{idea}

List top 5 risks.

Return JSON:
{{
  "technical_risks": [],
  "business_risks": []
}}
"""

    response = client.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT}
    ])

    content = clean_json(response.content)

    try:
        parsed = json.loads(content)
        validated = RiskOutput(**parsed)
        return validated.dict()
    except (json.JSONDecodeError, ValidationError):
        return {
            "error": "Risk parsing failed",
            "raw_output": content
        }