from rag.retriever import get_retriever

from agents.clarification_agent import generate_clarifications
from agents.mvp_agent import generate_mvp
from agents.tech_stack_agent import generate_tech_stack
from agents.risk_agent import generate_risks
from agents.report_agent import generate_report

from tools.complexity_estimator import estimate_complexity
from tools.timeline_calculator import calculate_timeline
from tools.cost_estimator import estimate_cost


retriever = get_retriever()


def run_pipeline(idea: str, country="US"):

    
    docs = retriever.invoke(idea)
    context = "\n".join([doc.page_content for doc in docs])

    
    clarifications = generate_clarifications(idea)
    if "error" in clarifications:
        return {"error": "Clarification Agent Failed", "details": clarifications}

    
    mvp = generate_mvp(idea, context)
    if "error" in mvp:
        return {"error": "MVP Agent Failed", "details": mvp}

   
    tech_stack = generate_tech_stack(idea, context)
    if "error" in tech_stack:
        return {"error": "Tech Stack Agent Failed", "details": tech_stack}

    
    risks = generate_risks(idea)
    if "error" in risks:
        return {"error": "Risk Agent Failed", "details": risks}

    
    feature_count = len(mvp.get("core_features", []))

    
    complexity_data = estimate_complexity(
        feature_count,
        mvp.get("ai_features", False),
        mvp.get("integrations", 0)
    )

    complexity_level = complexity_data["level"]

    timeline = calculate_timeline(complexity_level)

    cost_data = estimate_cost(complexity_level, country=country)

    
    structured_data = {
        "idea": idea,
        "clarifications": clarifications,
        "mvp": mvp,
        "tech_stack": tech_stack,
        "risks": risks,
        "complexity": complexity_data,   # includes score + level
        "timeline": timeline,
        "estimated_cost": cost_data
    }

    
    investor_report = generate_report(structured_data)
    if "error" in investor_report:
        return {"error": "Report Agent Failed", "details": investor_report}

    
    return {
        "analysis": structured_data,
        "investor_report": investor_report
    }