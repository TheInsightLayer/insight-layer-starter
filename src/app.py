# Entry point: app.py
"""
Insight Layer LangGraph Prototype

This script demonstrates a prototype implementation of the Insight Layer
using a modular memory system to simulate how AI agents can reuse and contribute meaningful 
insights across tasks. 

Key Components:
- Parses task context from a user prompt
- Retrieves relevant InsightUnits from a shared memory vault
- Injects insights into prompt construction
- Executes an agent task with contextual awareness
- Summarizes and stores a new InsightUnit to memory

The prototype enables structured memory reuse between agents, emulating a form of collective, 
purpose-driven intelligence.
"""

import os
from datetime import datetime
from openai import OpenAI
from src.graph.task_parser import parse_task  # replace if parse_task is local
from src.graph.prompt_constructor import construct_prompt  # replace if overridden
from src.memory.insight_layer_memory import InsightLayerMemory
from dotenv import load_dotenv


load_dotenv()

# --- Task Agent ---
def run_task(prompt, task_meta=None):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=openai_api_key)

    purpose = task_meta.get("purpose", "assistant") if task_meta else "assistant"
    system_msg = f"You are an assistant specializing in {purpose}."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

# --- Output Summarizer ---
def summarize_output(output, context):
    return {
        "who": "Insight Agent",
        "what": output.splitlines()[0][:80] if output else "Generated insight",
        "when": datetime.now().strftime("%Y-%m-%d"),
        "why": context.get("purpose", "general"),
        "how": "Generated based on past insights and agent reasoning.",
        "outcome": "Pending execution",
        "source": output
    }

# --- Prompt Constructor ---
def construct_prompt(task, insights):
    if insights:
        insight_text = "\n".join(
            [f"- {i['who']} did {i['what']} because {i['why']} (Outcome: {i['outcome']})" for i in insights]
        )
        return f"Use the following prior insights:\n{insight_text}\n\nTask: {task}"
    else:
        return f"No prior insights found.\n\nTask: {task}"

# --- Task Parser (simple placeholder or override if imported) ---
def parse_task(prompt):
    return {
        "purpose": "campaign planning",
        "quarter": "Q3",
        "topic": "customer retention"
    }

# --- Main Logic ---
def main():
    user_input = "Create a customer retention campaign for Q3."
    task_meta = parse_task(user_input)

    memory = InsightLayerMemory()  # vault_path is optional if defaulted

    # Load relevant insights
    insights = memory.load_context(task_meta)

    # Construct prompt
    enriched_prompt = construct_prompt(user_input, insights)

    # Run agent with prompt and metadata
    agent_output = run_task(enriched_prompt, task_meta)

    # Summarize and store new insight
    new_insight = summarize_output(agent_output, task_meta)
    memory.save_context(new_insight)

    print("\n--- Agent Output ---\n")
    print(agent_output)
    print("\n--- Insight Stored ---\n")
    print(new_insight)


if __name__ == "__main__":
    main()
