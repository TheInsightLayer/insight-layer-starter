
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4", temperature=0.2)

def infer_task_meta(task_string: str) -> dict:
    prompt = PromptTemplate.from_template("""
You are an assistant extracting metadata from a task string.

Task: "{task_string}"

Extract the following:
- Purpose (e.g. 'campaign planning', 'strategy', 'analysis')
- Topic (one or two words, like 'retention', 'loyalty', 'revenue')
- Quarter (e.g. Q1, Q2, or 'None' if not mentioned)

Respond in JSON format with keys: purpose, topic, quarter.
""")
    response = llm.predict(prompt.format(task_string=task_string))

    try:
        import json
        result = json.loads(response)
        return {
            "purpose": result.get("purpose", "general"),
            "topic": result.get("topic", "general"),
            "quarter": result.get("quarter", "None")
        }
    except Exception as e:
        print("[meta inference error]", e)
        return {
            "purpose": "general",
            "topic": "general",
            "quarter": "None"
        }

# Example usage
if __name__ == "__main__":
    task = "Create a campaign to improve Q3 customer loyalty"
    print(infer_task_meta(task))
