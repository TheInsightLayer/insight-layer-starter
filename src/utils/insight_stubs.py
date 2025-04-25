import uuid
import re
from datetime import datetime
from src.models.insight_unit import InsightUnit

def fallback_parse(prompt: str) -> dict:
    """Extracts minimal task meta from user input."""
    quarter_match = re.search(r'\bQ[1-4]\b', prompt, re.IGNORECASE)
    quarter = quarter_match.group(0).upper() if quarter_match else "unspecified"
    topic = "customer retention" if "retention" in prompt.lower() else "unspecified"
    purpose = "campaign planning" if "campaign" in prompt.lower() else "general task"
    return {"purpose": purpose, "topic": topic, "quarter": quarter}

def create_stub_insight(prompt: str) -> InsightUnit:
    """Generates a schema-valid stub InsightUnit from a prompt."""
    task_meta = fallback_parse(prompt)
    insight_id = f"insight_{uuid.uuid4().hex[:8]}"

    return InsightUnit(
        schema_version="v1.1",
        id=insight_id,
        title=f"Stub: {task_meta['topic'].title()} Insight",
        type="PromptAnchor",
        status="active",
        tags=["auto", task_meta["topic"]],
        content={
            "summary": f"Stub insight for: {prompt}",
            "key_takeaways": ["Auto-generated", "Awaiting completion"],
            "origin_method": "parsed_from_prompt",
            "source_systems": ["prompt"],
            "supporting_evidence": []
        },
        confidence={
            "confidence_level": "speculative",
            "confidence_score": 0.0,
            "validation_method": None,
            "validation_date": None,
            "linked_outcome": "pending"
        },
        fidelity={
            "fidelity_level": "speculative",
            "source_match_score": 0.5,
            "verified_by": [],
            "date_validated": None,
            "fidelity_review_needed": True
        },
        prompt={
            "prompt_tags": [task_meta["topic"]],
            "suggested_prompt_formats": [f"What should we do for {task_meta['topic']}?"],
            "grounding_phrases": [],
            "copilot_priority": "low"
        },
        business_context={"division": "General", "region": "US"},
        audience_profiles=["Analyst"],
        onboarding_relevance=50,
        security_classification="internal",
        confidentiality="team_only"
    )
