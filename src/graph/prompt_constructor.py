def construct_prompt(task: str, insights: list, purpose: str = "general") -> str:
    """
    Constructs a context-aware prompt for the agent using relevant insights.

    Parameters:
        task (str): A natural language task or instruction.
        insights (list): A list of prior insights (dicts).
        purpose (str): Optional task purpose (e.g., 'campaign planning', 'engineering') 
                       used to personalize the tone of the prompt.

    Returns:
        str: A formatted prompt for LLM input.
    """

    # Choose intro message based on task purpose
    purpose_templates = {
        "campaign planning": "You are planning a strategic marketing campaign.",
        "product analysis": "You are evaluating product performance and improvements.",
        "engineering decision": "You are making a technical implementation choice.",
        "general": "You are working on a task using available organizational knowledge."
    }
    intro = purpose_templates.get(purpose.lower(), purpose_templates["general"])

    # Format prior insights into bullet points
    if insights:
        context_lines = [
            f"- {i['who']} did {i['what']} because {i['why']} (Outcome: {i['outcome']})"
            for i in insights
        ]
        context_block = "\n".join(context_lines)
    else:
        context_block = "No prior insights were found for this task context."

    # Assemble full prompt
    return f"{intro}\n\nPrior Insights:\n{context_block}\n\nTask:\n{task}"
