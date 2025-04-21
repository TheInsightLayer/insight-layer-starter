
from openai import OpenAI
import os
import json
import time
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def fallback_parse(prompt: str) -> dict:
    quarter_match = re.search(r'\bQ[1-4]\b', prompt, re.IGNORECASE)
    quarter = quarter_match.group(0).upper() if quarter_match else "unspecified"
    topic = "customer retention" if "retention" in prompt.lower() else "unspecified"
    purpose = "campaign planning" if "campaign" in prompt.lower() else "general task"
    return {"purpose": purpose, "topic": topic, "quarter": quarter}

def parse_task(prompt: str, use_llm: bool = True, max_retries: int = 2) -> dict:
    if not use_llm:
        return fallback_parse(prompt)

    system_prompt = (
        "You are an AI that extracts structured metadata from user instructions.\n"
        "Return a JSON object with keys: purpose, topic, and quarter.\n"
    )
    for attempt in range(max_retries + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return json.loads(response.choices[0].message.content.strip())
        except Exception as e:
            if attempt == max_retries:
                fallback = fallback_parse(prompt)
                fallback["error"] = f"LLM failed after {max_retries+1} attempts: {str(e)}"
                return fallback
            time.sleep(1)
