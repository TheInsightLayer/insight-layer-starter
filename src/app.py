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
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from src.graph.task_parser import parse_task
from src.graph.prompt_constructor import construct_prompt
from src.memory.summarizer import summarize_and_normalize
from src.memory.insight_layer_memory import InsightLayerMemory
from src.utils.normalize_fields import normalize_insight


# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

# --- Task Agent ---
def run_task(prompt, task_meta=None):
    client = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4")
    purpose = task_meta.get("purpose", "assistant") if task_meta else "assistant"
    system_msg = f"You are an assistant specializing in {purpose}."
    response = client([SystemMessage(content=system_msg), HumanMessage(content=prompt)])
    return response.content.strip()

# --- Main Logic ---
def main():
    user_input = "Create a customer retention campaign for Q3."
    task_meta = parse_task(user_input)

    memory = InsightLayerMemory()
    insights = memory.load_context(task_meta)

    enriched_prompt = construct_prompt(user_input, insights)
    agent_output = run_task(enriched_prompt, task_meta)

    # Create, normalize, and store new insight
    raw_insight = summarize_and_normalize(agent_output, task_meta)
    normalized_insight = normalize_insight(raw_insight)
    memory.save_context(normalized_insight)

    print("\n--- Agent Output ---\n")
    print(agent_output)
    print("\n--- Insight Stored ---\n")
    print(normalized_insight)

if __name__ == "__main__":
    main()
