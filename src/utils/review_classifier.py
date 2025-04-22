from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
import json
import logging
import time
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4")

def load_thresholds(config_path: str = "configs/review_thresholds.json") -> Dict[str, Any]:
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Failed to load thresholds: {str(e)}")
        return {
            "auto_approve_confidence": 0.7,
            "auto_approve_max_sensitivity": 0.4,
            "ingestion_min_confidence": 0.6,
            "default_review_status": "pending"
        }

def call_llm_with_retry(prompt: str, retries: int = 3, delay: int = 2) -> Any:
    for attempt in range(retries):
        try:
            response = client([
                SystemMessage(content="You are a safety-aware AI reviewer for organizational insights."),
                HumanMessage(content=prompt)
            ])
            return response
        except Exception as e:
            logger.warning(f"LLM call failed on attempt {attempt + 1}: {str(e)}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise

def auto_score_review(insight: Dict[str, str]) -> Dict[str, Any]:
    """
    Uses GPT-4 to evaluate an InsightUnit for confidence and sensitivity,
    and recommends a review_status based on configured thresholds.

    Config keys used:
    - auto_approve_confidence
    - auto_approve_max_sensitivity
    - ingestion_min_confidence
    - default_review_status

    Returns:
        {
            "confidence_score": float,
            "sensitivity_score": float,
            "review_status": str
        }
    """

    thresholds = load_thresholds()  # Loads from configs/review_thresholds.json
    logger.info("Starting auto_score_review for insight.")
    logger.debug(f"Insight data: {insight}")
    logger.debug(f"Loaded thresholds: {thresholds}")

    required_fields = ["who", "what", "why", "how", "outcome"]
    missing_fields = [field for field in required_fields if field not in insight]
    if missing_fields:
        raise ValueError(f"Missing required fields in insight: {', '.join(missing_fields)}")

    auto_conf = thresholds.get("auto_approve_confidence", 0.7)
    max_sens = thresholds.get("auto_approve_max_sensitivity", 0.4)
    min_conf = thresholds.get("ingestion_min_confidence", 0.6)
    default_status = thresholds.get("default_review_status", "pending")

    prompt = f"""
Evaluate the following insight for sensitivity and confidence.

Insight:
Who: {insight.get("who")}
What: {insight.get("what")}
Why: {insight.get("why")}
How: {insight.get("how")}
Outcome: {insight.get("outcome")}

Return a JSON object with:
- sensitivity_score: float (0 = not sensitive, 1 = highly sensitive)
- confidence_score: float (0 = low confidence, 1 = very confident)
"""

    try:
        response = call_llm_with_retry(prompt)
        try:
            content = response.content.strip()
            result = json.loads(content)
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"Invalid LLM response: {str(e)}")
            return {
                "confidence_score": 0.0,
                "sensitivity_score": 0.5,
                "review_status": default_status,
                "error": f"Invalid LLM response: {str(e)}"
            }

        conf = result.get("confidence_score", 0.0)
        sens = result.get("sensitivity_score", 0.5)

        if conf >= auto_conf and sens <= max_sens:
            result["review_status"] = "auto"
        elif conf < min_conf:
            result["review_status"] = "rejected"
        else:
            result["review_status"] = default_status

        return result

    except Exception as e:
        logger.error(f"LLM scoring failed: {str(e)}")
        return {
            "confidence_score": 0.0,
            "sensitivity_score": 0.5,
            "review_status": default_status,
            "error": f"LLM scoring failed: {str(e)}"
        }

def test_auto_score_review_valid(monkeypatch):
    def mock_load_thresholds():
        return {
            "auto_approve_confidence": 0.7,
            "auto_approve_max_sensitivity": 0.4,
            "ingestion_min_confidence": 0.6,
            "default_review_status": "pending"
        }

    def mock_call_llm_with_retry(prompt):
        return {
            "choices": [
                {"message": {"content": '{"confidence_score": 0.8, "sensitivity_score": 0.3}'}}
            ]
        }

    monkeypatch.setattr("src.utils.review_classifier.load_thresholds", mock_load_thresholds)
    monkeypatch.setattr("src.utils.review_classifier.call_llm_with_retry", mock_call_llm_with_retry)

    insight = {"who": "User", "what": "Test insight", "why": "Reason", "how": "Method", "outcome": "Result"}
    result = auto_score_review(insight)
    assert result["review_status"] == "auto"

def test_auto_score_review_missing_fields():
    insight = {"what": "Test insight"}
    with pytest.raises(ValueError, match="Missing required fields"):
        auto_score_review(insight)

def test_auto_score_review_invalid_llm_response(monkeypatch):
    def mock_call_llm_with_retry(prompt):
        return {"choices": [{"message": {"content": "Invalid JSON"}}]}

    monkeypatch.setattr("src.utils.review_classifier.call_llm_with_retry", mock_call_llm_with_retry)

    insight = {"who": "User", "what": "Test insight", "why": "Reason", "how": "Method", "outcome": "Result"}
    result = auto_score_review(insight)
    assert result["review_status"] == "pending"
    assert "error" in result
