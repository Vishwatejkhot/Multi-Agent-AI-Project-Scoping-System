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


class TechStackOutput(BaseModel):
    frontend: str
    backend: str
    database: str
    ai_layer: str
    hosting: str


SYSTEM_PROMPT = """
You are a Senior Software Architect.

Suggest a realistic, scalable, and cost-aware tech stack.

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


def generate_tech_stack(idea: str, context: str):

    USER_PROMPT = f"""
Startup Idea:
{idea}

Relevant Best Practices Context:
{context}

Return JSON:
{{
  "frontend": "",
  "backend": "",
  "database": "",
  "ai_layer": "",
  "hosting": ""
}}
"""

    response = client.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT}
    ])

    content = clean_json(response.content)

    try:
        parsed = json.loads(content)
        validated = TechStackOutput(**parsed)
        return validated.dict()
    except (json.JSONDecodeError, ValidationError):
        return {
            "error": "Tech stack parsing failed",
            "raw_output": content
        }