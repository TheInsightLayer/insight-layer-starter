from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
import json
import time
import re
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4")

def fallback_parse(prompt: str) -> Dict[str, str]:
    quarter_match = re.search(r'\bQ[1-4]\b', prompt, re.IGNORECASE)
    quarter = quarter_match.group(0).upper() if quarter_match else "unspecified"
    topic = "customer retention" if "retention" in prompt.lower() else "unspecified"
    purpose = "campaign planning" if "campaign" in prompt.lower() else "general task"
    return {"purpose": purpose, "topic": topic, "quarter": quarter}

def parse_task(prompt: str, use_llm: bool = True, max_retries: int = 2) -> Dict[str, str]:
    if not use_llm:
        return fallback_parse(prompt)

    system_prompt = (
        "You are an AI that extracts structured metadata from user instructions.\n"
        "Return a JSON object with keys: purpose, topic, and quarter.\n"
    )
    for attempt in range(max_retries + 1):
        try:
            response = client([
                SystemMessage(content=system_prompt),
                HumanMessage(content=prompt)
            ])
            return json.loads(response.content.strip())
        except Exception as e:
            if attempt == max_retries:
                fallback = fallback_parse(prompt)
                fallback["error"] = f"LLM failed after {max_retries+1} attempts: {str(e)}"
                return fallback
            time.sleep(1)
