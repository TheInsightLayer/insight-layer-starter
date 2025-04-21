
from src.memory.insight_layer_memory import InsightLayerMemory
from typing import List, Dict, Optional, Union
import time
from functools import lru_cache

# Internal function that performs actual filtering
def _retrieve_filtered_insights(
    purpose: str,
    topic: str,
    quarter: str,
    role: Optional[str] = None,
    min_importance: Optional[float] = None,
    max_age_days: Optional[int] = None
) -> List[Dict]:
    memory = InsightLayerMemory(vault_path="data/memory.db")
    task_meta = {"purpose": purpose, "topic": topic, "quarter": quarter}
    all_insights = memory.load_context(task_meta)

    now = time.time()
    filtered = []

    for insight in all_insights:
        if role and role not in insight.get("roles", []):
            continue
        if min_importance is not None and insight.get("importance_score", 0) < min_importance:
            continue
        if max_age_days:
            timestamp = insight.get("timestamp")
            if timestamp and (now - timestamp > max_age_days * 86400):
                continue
        filtered.append(insight)

    return filtered

# Cached version for direct use
@lru_cache(maxsize=64)
def retrieve_insights_cached(
    purpose: str,
    topic: str,
    quarter: str,
    role: Optional[str] = None,
    min_importance: Optional[float] = None,
    max_age_days: Optional[int] = None
) -> List[Dict]:
    return _retrieve_filtered_insights(purpose, topic, quarter, role, min_importance, max_age_days)

# Tool-compatible entry point
def retrieve_insights(
    purpose: Optional[str] = None,
    topic: Optional[str] = None,
    quarter: Optional[str] = None,
    role: Optional[str] = None,
    min_importance: Optional[float] = None,
    max_age_days: Optional[int] = None,
    input_dict: Optional[dict] = None
) -> List[Dict]:
    """
    Dual-mode insight retriever that supports both direct use and LangChain tool input.

    If called with input_dict, disables caching for LangChain compatibility.
    Otherwise, uses a cached path for performance in script or CLI usage.
    """
    if input_dict:
        return _retrieve_filtered_insights(
            input_dict.get("purpose", ""),
            input_dict.get("topic", ""),
            input_dict.get("quarter", ""),
            input_dict.get("role"),
            input_dict.get("min_importance"),
            input_dict.get("max_age_days")
        )

    return retrieve_insights_cached(
        purpose or "", topic or "", quarter or "",
        role, min_importance, max_age_days
    )
