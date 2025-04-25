"""
Wrapper for insight summarization at the memory level.
Delegates to the full summarizer in the graph layer and normalizes the output.
"""

from src.graph.summarizer import summarize_output

def summarize_and_normalize(agent_output: str, task_meta: dict) -> dict:
    """
    Use LLM (or fallback) to summarize agent output into an InsightUnit,
    then normalize and return it.
    """
    return summarize_output(
        output=agent_output,
        context=task_meta,
        use_llm=True,
        trace_enabled=False
    )
