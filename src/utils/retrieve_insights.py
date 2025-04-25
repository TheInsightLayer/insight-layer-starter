# src/utils/retrieve_insights.py

from typing import List, Optional
from datetime import datetime, timedelta
from src.memory.insight_layer_memory import InsightLayerMemory
from src.utils.scoring import compute_importance

memory = InsightLayerMemory()

def retrieve_insights(
    purpose: str,
    topic: str,
    quarter: str,
    role: Optional[str] = None,
    min_importance: Optional[float] = None,
    max_age_days: Optional[int] = None
) -> List[dict]:
    """
    Retrieves insights matching metadata filters and optionally applies scoring.

    Args:
        purpose: The goal of the task (e.g. "campaign planning")
        topic: The focus of the task (e.g. "promotion")
        quarter: Time filter (e.g. "Q1")
        role: Optional role filter (e.g. "MSL")
        min_importance: Minimum score to include insight (0-1)
        max_age_days: Only include insights newer than this many days

    Returns:
        List of filtered InsightUnits
    """

    all_insights = memory.load_context({
        "purpose": purpose,
        "topic": topic,
        "quarter": quarter
    })

    filtered = []
    now = datetime.now()

    for insight in all_insights:
        # Check role filter
        if role:
            roles = insight.get("narrative", {}).get("roles") or insight.get("audience_profiles", [])
            if role not in roles:
                continue

        # Check recency filter
        when = insight.get("narrative", {}).get("when")
        if max_age_days and when:
            try:
                insight_date = datetime.strptime(when, "%Y-%m-%d")
                if (now - insight_date).days > max_age_days:
                    continue
            except Exception:
                pass  # Ignore if date format is bad

        # Compute importance and filter if too low
        score = compute_importance(insight)
        if min_importance is not None and score < min_importance:
            continue

        insight["importance_score"] = score
        filtered.append(insight)

    return filtered
