
from src.graph.retriever import retrieve_insights

def recommend_insights_node(state: dict) -> dict:
    """
    LangGraph node that pulls top relevant insights based on task_meta
    and adds them to the state as 'recommended_insights'.

    This node does NOT use an LLM and is safe for pre-task enrichment.
    """
    task_meta = state.get("task_meta", {})
    role = state.get("role")
    min_importance = state.get("min_importance")
    max_age_days = state.get("max_age_days")
    top_n = state.get("top_n", 3)

    insights = retrieve_insights(
        purpose=task_meta.get("purpose", ""),
        topic=task_meta.get("topic", ""),
        quarter=task_meta.get("quarter", ""),
        role=role,
        min_importance=min_importance,
        max_age_days=max_age_days
    )

    # Basic explanations (LLM-ready version could be added)
    def explain(insight):
        return f"{insight['what']} (Why: {insight.get('why')}, Outcome: {insight.get('outcome')})"

    state["recommended_insights"] = [
        {
            "what": i["what"],
            "why": i.get("why"),
            "outcome": i.get("outcome"),
            "explanation": explain(i)
        }
        for i in insights[:top_n]
    ]

    return state
