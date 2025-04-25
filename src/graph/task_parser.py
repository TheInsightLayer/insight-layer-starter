from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import json
import re
import uuid

# Load environment variables
load_dotenv()
client = ChatOpenAI(
    model="gpt-4",
    temperature=0.3,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# -- Fallback method if LLM fails --
def fallback_parse(prompt: str) -> dict:
    quarter_match = re.search(r'\bQ[1-4]\b', prompt, re.IGNORECASE)
    quarter = quarter_match.group(0).upper() if quarter_match else "None"
    topic = "loyalty" if "loyalty" in prompt.lower() else "general"
    purpose = "campaign planning" if "campaign" in prompt.lower() or "promotion" in prompt.lower() else "general"
    return {
        "purpose": purpose,
        "topic": topic,
        "quarter": quarter
    }

# -- Main parsing function --
def parse_task(prompt: str) -> dict:
    """
    Attempts to extract task metadata (purpose, topic, quarter) from a prompt using OpenAI,
    and falls back to keyword matching if that fails.
    """
    system_msg = "You are a helpful assistant extracting metadata from a business prompt."
    user_msg = f"""
Prompt: "{prompt}"

Return only JSON with keys:
- purpose (e.g. 'campaign planning', 'analytics', 'research')
- topic (e.g. 'loyalty', 'retention', 'promotion')
- quarter (e.g. 'Q1', 'Q2', or 'None' if not specified)
"""

    try:
        response = client.invoke([
            SystemMessage(content=system_msg),
            HumanMessage(content=user_msg)
        ])
        parsed = json.loads(response.content)

        return {
            "purpose": parsed.get("purpose", "general"),
            "topic": parsed.get("topic", "general"),
            "quarter": parsed.get("quarter", "None")
        }

    except Exception as e:
        print("[parse_task fallback]", e)
        return fallback_parse(prompt)

# Example usage
if __name__ == "__main__":
    example = "Design a Q2 promotion strategy to boost loyalty"
    print(parse_task(example))
