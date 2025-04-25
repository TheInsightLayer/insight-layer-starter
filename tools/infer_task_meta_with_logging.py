
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4", temperature=0.2)

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
        log = {
            "input": task_string,
            "output": result
        }
        with open(log_path, "a") as f:
            f.write(json.dumps(log) + "\n")

        return {
            "purpose": result.get("purpose", "general"),
            "topic": result.get("topic", "general"),
            "quarter": result.get("quarter", "None"),
            "confidence": result.get("confidence", 5)
        }
    except Exception as e:
        print("[meta inference error]", e)
        return {
            "purpose": "general",
            "topic": "general",
            "quarter": "None",
            "confidence": 0
        }
