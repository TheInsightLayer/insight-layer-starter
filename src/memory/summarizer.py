from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
import json
import time
from typing import Dict
from src.utils.review_classifier import auto_score_review

client = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4")

def fallback_summarize(output: str, context: Dict[str, str]) -> Dict[str, str]:
    return {
        "who": "Insight Agent",
        "what": output.split(".")[0][:60] if output else "Unstructured insight",
        "when": context.get("timestamp", "unknown"),
        "why": context.get("purpose", "unknown"),
        "how": "Summarized manually",
        "outcome": "undetermined",
        "source": output
    }

def summarize_output(output: str, context: Dict[str, str], use_llm: bool = True, max_retries: int = 2) -> Dict[str, str]:
    if not use_llm:
        return fallback_summarize(output, context)

    system_prompt = (
        "You are an AI that summarizes task output into a structured InsightUnit.\n"
        "Return JSON with keys: who, what, when, why, how, outcome.\n"
    )
    user_prompt = f"Context: {context}\n\nOutput: {output}"
    for attempt in range(max_retries + 1):
        try:
            response = client([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            summary = json.loads(response.content.strip())
            review = auto_score_review(summary)
            summary.update(review)
            return summary
        except Exception as e:
            if attempt == max_retries:
                fallback = fallback_summarize(output, context)
                fallback["error"] = f"LLM failed after {max_retries+1} attempts: {str(e)}"
                return fallback
            time.sleep(1)
