
from langchain.tools import Tool
from src.utils.retrieve_insights import retrieve_insights  # Adjust path if needed

# Define a LangChain-compatible tool for insight retrieval
retrieve_insights_tool = Tool(
    name="InsightRetriever",
    func=lambda input_dict: retrieve_insights(
        purpose=input_dict.get("purpose", ""),
        topic=input_dict.get("topic", ""),
        quarter=input_dict.get("quarter", ""),
        role=input_dict.get("role"),
        min_importance=input_dict.get("min_importance"),
        max_age_days=input_dict.get("max_age_days")
    ),
    description="""
    Retrieve relevant organizational insights from memory based on task metadata.

    Required keys:
    - purpose: the goal of the task
    - topic: the topic or subject area
    - quarter: time period for filtering (e.g., 'Q1')

    Optional keys:
    - role: filter insights for a specific persona
    - min_importance: minimum score threshold (0-1)
    - max_age_days: ignore older insights

    Returns a list of filtered InsightUnits.
    """
)
