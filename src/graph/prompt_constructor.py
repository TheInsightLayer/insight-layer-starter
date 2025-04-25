# src/graph/prompt_constructor.py

from typing import List, Dict

def construct_prompt(task: str, insights: List[Dict], purpose: str = "general") -> str:
    """
    Constructs a context-aware prompt for the agent using structured insights.

    Parameters:
        task (str): The natural language instruction or problem.
        insights (list): A list of prior structured InsightUnits (dicts).
        purpose (str): The task's general purpose, used to frame the system's perspective.

    Returns:
        str: A formatted LLM prompt incorporating prior context and the new task.
    """

    # Step 1: Set task framing by purpose
    purpose_templates = {
        "campaign planning": "You are planning a marketing or engagement campaign using past learnings.",
        "strategy": "You are developing an organizational strategy informed by historical insights.",
        "engineering": "You are making an implementation decision based on previously validated patterns.",
        "general": "You are solving a business task using available internal knowledge."
    }
    intro = purpose_templates.get(purpose.lower(), purpose_templates["general"])

    # Step 2: Format relevant insights into structured bullets
    if insights:
        context_lines = []
        for i in insights:
            summary = i.get("content", {}).get("summary", i.get("what", "Insight summary missing"))
            why = i.get("narrative", {}).get("why", i.get("why", "reason unknown"))
            outcome = i.get("confidence", {}).get("linked_outcome", i.get("narrative", {}).get("outcome", "outcome unknown"))
            fidelity = i.get("fidelity", {}).get("fidelity_level", "N/A")
            source = ", ".join(i.get("content", {}).get("source_systems", [])) or "unspecified source"

            line = f"- {summary} (Why: {why}, Outcome: {outcome}, Fidelity: {fidelity}, Source: {source})"
            context_lines.append(line)

        context_block = "\n".join(context_lines)
    else:
        context_block = "No prior insights found for this task."

    # Step 3: Return the complete system prompt
    return f"""{intro}

Prior Insights:
{context_block}

Your Task:
{task}

Use the prior insights to inform your recommendation. Be concise, structured, and refer back to relevant examples if helpful.
"""
