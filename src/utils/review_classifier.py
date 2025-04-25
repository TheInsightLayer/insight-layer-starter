from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os, json, logging, time
from typing import Dict, Any

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
            response = client.invoke([
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
    thresholds = load_thresholds()
    logger.info("Scoring insight for confidence and sensitivity.")

    required_fields = ["who", "what", "why", "how", "outcome"]
    missing_fields = [field for field in required_fields if field not in insight]
    if missing_fields:
        raise ValueError(f"Missing required fields in insight: {', '.join(missing_fields)}")

    auto_conf = thresholds["auto_approve_confidence"]
    max_sens = thresholds["auto_approve_max_sensitivity"]
    min_conf = thresholds["ingestion_min_confidence"]
    default_status = thresholds["default_review_status"]

    prompt = f"""
Evaluate the following insight for sensitivity and confidence.

Insight:
Who: {insight['who']}
What: {insight['what']}
Why: {insight['why']}
How: {insight['how']}
Outcome: {insight['outcome']}

Return a JSON object with:
- sensitivity_score: float (0 = not sensitive, 1 = highly sensitive)
- confidence_score: float (0 = low confidence, 1 = very confident)
"""

    try:
        response = call_llm_with_retry(prompt)
        content = response.content.strip()
        result = json.loads(content)

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
