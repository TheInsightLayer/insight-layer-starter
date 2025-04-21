
from langchain.tools import Tool
from src.graph.retriever import retrieve_insights

def explain_relevance(insight):
    # Simple explanation logic; can be replaced with an LLM
    return f"This was used for {insight.get('why', 'a similar purpose')} and had outcome: {insight.get('outcome', 'unknown')}."

def recommend_insights_tool(input_dict):
    insights = retrieve_insights(input_dict=input_dict)
    top_n = input_dict.get("top_n", 3)

    summaries = []
    for insight in insights[:top_n]:
        summaries.append({
            "what": insight["what"],
            "why": insight.get("why"),
            "outcome": insight.get("outcome"),
            "explanation": explain_relevance(insight)
        })

    return summaries

insight_recommender_tool = Tool(
    name="InsightRecommender",
    func=recommend_insights_tool,
    description="""
    Recommends top N relevant insights based on task metadata:
    Required keys:
        - purpose (str)
        - topic (str)
        - quarter (str)
    Optional:
        - role (str)
        - min_importance (float)
        - max_age_days (int)
        - top_n (int, default=3)
    Returns:
        A list of structured, relevant insights with plain-language explanations.
    """
)
