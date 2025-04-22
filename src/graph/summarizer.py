import os
import json
import time
from datetime import datetime
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from typing import Optional
from src.utils.review_classifier import auto_score_review  # Adds post-summary scoring logic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LangChain OpenAI API client
client = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4")

# Trace log (summarization process)
TRACE_SUMMARY_PATH = "data/trace_logs/summaries"
# Outcome log (was this insight useful?)
SUMMARY_OUTCOME_PATH = "data/trace_logs/summary_outcomes"

os.makedirs(TRACE_SUMMARY_PATH, exist_ok=True)
os.makedirs(SUMMARY_OUTCOME_PATH, exist_ok=True)

def fallback_summarize(output: str, context: dict) -> dict:
    """
    Generates a basic insight summary using fallback logic.
    Used if LLM summarization is disabled or fails.
    """
    return {
        "who": "Insight Agent",
        "what": output.split(".")[0][:60] if output else "Unstructured insight",
        "when": context.get("timestamp", "unknown"),
        "why": context.get("purpose", "unknown"),
        "how": "Summarized manually",
        "outcome": "undetermined",
        "source": output,
        "was_useful": None  # Placeholder for future feedback
    }

def log_summary_trace(summary: dict, context: dict, trace_id: Optional[str] = None):
    """
    Saves a trace log of the summarization process.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    trace_name = trace_id or f"summary_{timestamp}.json"
    trace_path = os.path.join(TRACE_SUMMARY_PATH, trace_name)

    with open(trace_path, "w") as f:
        json.dump({
            "context": context,
            "summary": summary
        }, f, indent=2)

def log_summary_outcome(summary: dict, outcome: str = "pending", source: str = "agent"):
    """
    Stores an outcome log that can be updated over time.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = os.path.join(SUMMARY_OUTCOME_PATH, f"outcome_{timestamp}.json")
    entry = {
        "summary_id": summary.get("id", summary.get("source", "unknown")),
        "outcome_feedback": outcome,
        "source": source,
        "logged_at": timestamp
    }
    with open(filename, "w") as f:
        json.dump(entry, f, indent=2)

def summarize_output(
    output: str,
    context: dict,
    use_llm: bool = True,
    max_retries: int = 2,
    trace_enabled: bool = False
) -> dict:
    """
    Summarizes task output into a structured InsightUnit using GPT-4 or fallback logic.
    Includes review scoring and optional trace logging.
    """
    # --- Manual fallback mode (no LLM) ---
    if not use_llm:
        summary = fallback_summarize(output, context)
        summary["confidence"] = 0.0
        if trace_enabled:
            log_summary_trace(summary, context)
        return summary

    # --- Prepare GPT prompt ---
    system_prompt = (
        "You are an AI that summarizes task output into a structured InsightUnit.\n"
        "Return JSON with keys: who, what, when, why, how, outcome."
    )
    user_prompt = f"Context: {context}\n\nOutput: {output}"

    for attempt in range(max_retries + 1):
        try:
            response = client([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])

            summary = json.loads(response.content.strip())

            # Add placeholder for prompt success feedback
            summary["confidence"] = 1.0
            summary["was_useful"] = None  # Future feedback signal

            # Add scoring tags
            review = auto_score_review(summary)
            summary.update(review)

            if trace_enabled:
                log_summary_trace(summary, context)
                log_summary_outcome(summary, outcome="pending")

            return summary

        except Exception as e:
            if attempt == max_retries:
                fallback = fallback_summarize(output, context)
                fallback["error"] = f"LLM failed after {max_retries+1} attempts: {str(e)}"
                fallback["confidence"] = 0.0
                fallback["was_useful"] = None
                if trace_enabled:
                    log_summary_trace(fallback, context)
                    log_summary_outcome(fallback, outcome="pending")
                return fallback

            time.sleep(1)
