import os
import json
import time
import uuid
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from src.utils.review_classifier import auto_score_review
from src.utils.normalize_fields import normalize_insight

# Load environment variables
load_dotenv()

client = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4")

TRACE_SUMMARY_PATH = "data/trace_logs/summaries"
SUMMARY_OUTCOME_PATH = "data/trace_logs/summary_outcomes"
os.makedirs(TRACE_SUMMARY_PATH, exist_ok=True)
os.makedirs(SUMMARY_OUTCOME_PATH, exist_ok=True)

def fallback_summarize(output: str, context: dict) -> dict:
    return {
        "who": "Insight Agent",
        "what": output.split(".")[0][:60] if output else "Unstructured insight",
        "when": context.get("timestamp", datetime.now().strftime("%Y-%m-%d")),
        "why": context.get("purpose", "general"),
        "how": "Summarized manually",
        "outcome": "undetermined",
        "source": output,
        "confidence": 0.0,
        "was_useful": None
    }

def log_summary_trace(summary: dict, context: dict, trace_id=None):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    trace_name = trace_id or f"summary_{timestamp}.json"
    trace_path = os.path.join(TRACE_SUMMARY_PATH, trace_name)
    with open(trace_path, "w") as f:
        json.dump({"context": context, "summary": summary}, f, indent=2)

def log_summary_outcome(summary: dict, outcome="pending", source="agent"):
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

def summarize_output(output: str, context: dict, use_llm: bool = True, max_retries: int = 2, trace_enabled: bool = False) -> dict:
    try:
        if not use_llm:
            summary = fallback_summarize(output, context)
        else:
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
                    summary.update(auto_score_review(summary))
                    summary["confidence"] = 1.0
                    summary["was_useful"] = None
                    break
                except Exception as e:
                    if attempt == max_retries:
                        summary = fallback_summarize(output, context)
                        summary["error"] = f"LLM failed after {max_retries+1} attempts: {str(e)}"
                        break
                    time.sleep(1)

        full_unit = {
            "schema_version": "v1.1",
            "id": f"insight_{uuid.uuid4().hex[:8]}",
            "title": summary["what"][:60],
            "type": "ObservedPattern",
            "status": "active",
            "tags": context.get("tags", [context.get("topic", "general")]),
            "content": {
                "summary": summary["what"],
                "key_takeaways": [summary.get("why", ""), summary.get("how", "")],
                "origin_method": "agent_generated",
                "source_systems": ["llm"],
                "supporting_evidence": []
            },
            "confidence": {
                "confidence_level": "generated",
                "confidence_score": summary.get("confidence", 1.0),
                "validation_method": "none",
                "validation_date": None,
                "linked_outcome": summary.get("outcome", "pending")
            },
            "narrative": summary,
            "business_context": {
                "division": context.get("division", "General"),
                "region": context.get("region", "US")
            },
            "confidentiality": "internal"
        }

        if trace_enabled:
            log_summary_trace(full_unit, context)
            log_summary_outcome(full_unit)

        return normalize_insight(full_unit)

    except Exception as err:
        return {"error": str(err)}
