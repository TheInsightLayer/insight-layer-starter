import os
import json
from datetime import datetime
from typing import List, Dict
from src.memory.insight_layer_memory import InsightLayerMemory

class InsightPusher:
    def __init__(self):
        self.memory = InsightLayerMemory()

    def recommend_insights(self, user_role: str, max_insights: int = 5) -> List[Dict]:
        """
        Recommend top relevant insights for a given user role.

        Parameters:
            user_role (str): The role of the user (e.g., "engineer", "product_manager").
            max_insights (int): Maximum number of insights to recommend.

        Returns:
            List[Dict]: A list of recommended insights.
        """
        insights = []

        # Load all insights from the memory directory
        for fname in os.listdir(self.memory.insight_dir):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(self.memory.insight_dir, fname)
            with open(fpath, "r") as f:
                insight = json.load(f)

                # Filter by role
                if user_role not in insight.get("roles", []):
                    continue

                # Filter by review status (e.g., only approved insights)
                if insight.get("review_status") != "approved":
                    continue

                # Calculate recency (only include insights from the last year)
                when = insight.get("when", "")
                if when:
                    try:
                        dt = datetime.strptime(when, "%Y-%m-%d")
                        days_ago = (datetime.now() - dt).days
                        if days_ago > 365:
                            continue
                    except Exception:
                        continue

                # Add the insight to the list
                insights.append(insight)

        # Sort insights by importance_score (descending)
        insights = sorted(insights, key=lambda x: x.get("importance_score", 0), reverse=True)

        # Return the top N insights
        return insights[:max_insights]

# Example usage
if __name__ == "__main__":
    pusher = InsightPusher()
    role = "engineer"
    recommendations = pusher.recommend_insights(user_role=role, max_insights=5)

    print(f"Top recommendations for role '{role}':")
    for insight in recommendations:
        print(f"- {insight['what']} (Score: {insight['importance_score']})")
