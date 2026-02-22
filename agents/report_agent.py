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


class ReportOutput(BaseModel):
    executive_summary: str
    problem_statement: str
    solution_overview: str
    mvp_summary: str
    technical_strategy: str
    risk_summary: str
    go_to_market_note: str
    investor_readiness_score: int


SYSTEM_PROMPT = """
You are a startup investor and technical advisor.

Generate an investor-ready structured project report.

Be concise.
Be realistic.
Be professional.

Return ONLY valid JSON.
Do NOT use markdown.
Do NOT explain outside JSON.
"""


def clean_json(content: str):
    """
    Removes markdown code blocks if present.
    """
    content = content.strip()

    if content.startswith("```"):
        content = re.sub(r"```.*?\n", "", content)
        content = content.replace("```", "")

    return content.strip()


def generate_report(data: dict):

    USER_PROMPT = f"""
Project Data:
{json.dumps(data, indent=2)}

Generate:

1. Executive summary
2. Problem statement
3. Solution overview
4. MVP summary
5. Technical strategy
6. Risk summary
7. Go-to-market note
8. Investor readiness score (1-10)

Return JSON:
{{
  "executive_summary": "",
  "problem_statement": "",
  "solution_overview": "",
  "mvp_summary": "",
  "technical_strategy": "",
  "risk_summary": "",
  "go_to_market_note": "",
  "investor_readiness_score": 0
}}
"""

    response = client.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT}
    ])

    content = clean_json(response.content)

    try:
        parsed = json.loads(content)
        validated = ReportOutput(**parsed)
        return validated.dict()
    except (json.JSONDecodeError, ValidationError):
        return {
            "error": "Report parsing failed",
            "raw_output": content
        }