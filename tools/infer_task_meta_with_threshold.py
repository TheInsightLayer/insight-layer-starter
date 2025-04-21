
import json
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4", temperature=0.2)
CONFIDENCE_THRESHOLD = int(os.getenv("MIN_CONFIDENCE_FOR_META", 6))
VERBOSE = os.getenv("VERBOSE", "false").lower() == "true"

def infer_task_meta(task_string: str, log_path: str = "data/inference_logs.json") -> dict:
    prompt = PromptTemplate.from_template("""
You are an assistant extracting metadata from a task string.

Task: "{task_string}"

Extract:
- Purpose (e.g. 'campaign planning', 'analysis')
- Topic (one or two words)
- Quarter (Q1–Q4 or 'None' if not mentioned)
- Confidence score from 1–10 (how confident are you?)

Return valid JSON: { "purpose": ..., "topic": ..., "quarter": ..., "confidence": ... }
""")
    response = llm.predict(prompt.format(task_string=task_string))

    try:
        result = json.loads(response)
        confidence = int(result.get("confidence", 0))

        if VERBOSE:
            print(f"[Inference confidence: {confidence}]")

        log = {
            "input": task_string,
            "output": result
        }
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a") as f:
            f.write(json.dumps(log) + "\n")

        if confidence >= CONFIDENCE_THRESHOLD:
            return {
                "purpose": result.get("purpose", "general"),
                "topic": result.get("topic", "general"),
                "quarter": result.get("quarter", "None"),
                "confidence": confidence
            }
        else:
            if VERBOSE:
                print(f"[⚠️ Confidence too low ({confidence} < {CONFIDENCE_THRESHOLD}) — returning fallback]")
            return {
                "purpose": "general",
                "topic": "general",
                "quarter": "None",
                "confidence": confidence
            }

    except Exception as e:
        print("[meta inference error]", e)
        return {
            "purpose": "general",
            "topic": "general",
            "quarter": "None",
            "confidence": 0
        }
