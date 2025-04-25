"""
    Dynamic Prompt Builder for Insight Layer

    This module constructs prompts based on task metadata and historical insight patterns.
    It replaces static prompt templates with context-aware, adaptive prompt logic.

    Key Features:
    - Loads prior InsightUnits and analyzes tone, format, and style
    - Builds new prompts using successful past patterns
    - Allows fallback to generic templates if needed
    """

import random
from typing import List, Dict

def extract_prompt_patterns(insights: List[Dict]) -> List[str]:
    return [i.get("prompt_style") for i in insights if i.get("prompt_style")] or ["general_summary"]

def build_dynamic_prompt(task: str, insights: List[Dict], task_meta: Dict) -> str:
    pattern = random.choice(extract_prompt_patterns(insights))

    context_lines = []
    for i in insights:
        if "narrative" in i:
            n = i["narrative"]
            context_lines.append(f"- {n['what']} (Why: {n.get('why', '-')}, Outcome: {n.get('outcome', '-')})")
        elif "content" in i:
            context_lines.append(f"- {i['content'].get('summary', '')}")

    context = "\n".join(context_lines) or "No prior insights available."

    if pattern == "bulleted_strategy":
        return f"""You are helping with {task_meta.get('purpose', 'a strategic task')}.

Use prior successful strategies:
{context}

Now generate a new strategy for: {task}"""

    elif pattern == "summary_plus_steps":
        return f"""Summarize relevant insights and outline next actions.

Context:
{context}

Task: {task}"""

    else:
        return f"""You are assisting with: {task}

Use context:
{context}"""

# Optional: Add scoring and feedback loop later to learn which prompts perform best