import yaml
import os
from datetime import datetime
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load weights from YAML if not provided directly
def load_importance_weights(path: str = os.getenv("IMPORTANCE_WEIGHTS_PATH", "configs/importance_weights.yaml")) -> Dict[str, float]:
    if os.path.exists(path):
        with open(path, "r") as f:
            return yaml.safe_load(f)
    else:
        # Fallback default weights
        return {
            "used": 0.4,
            "links": 0.3,
            "impact": 0.1,
            "outcome": 0.1,
            "recency": 0.1
        }

def compute_importance(insight: dict, weights: Optional[Dict[str, float]] = None) -> float:
    """
    Computes an importance score for a given insight based on usage, impact, links, etc.

    Parameters:
        insight (dict): An InsightUnit dictionary with relevant metadata.
        weights (dict, optional): If provided, overrides config weights.

    Returns:
        float: Rounded importance score.
    """
    if weights is None:
        weights = load_importance_weights()

    used = insight.get("used_count", 0)
    links = insight.get("linked_count", 0)
    impact = insight.get("impact_score", 5.0)
    outcome = insight.get("outcome_match", 0.5)
    when = insight.get("when", "")

    # Calculate recency decay (less weight for older)
    if when:
        try:
            dt = datetime.strptime(when, "%Y-%m-%d")
            days_ago = (datetime.now() - dt).days
            recency_weight = max(0.0, 1.0 - (days_ago / 365.0))  # 1 if today, 0 if over a year old
        except Exception:
            recency_weight = 0.5
    else:
        recency_weight = 0.5

    importance = (
        weights.get("used", 0) * used +
        weights.get("links", 0) * links +
        weights.get("impact", 0) * impact +
        weights.get("outcome", 0) * outcome +
        weights.get("recency", 0) * recency_weight
    )

    return round(importance, 2)
