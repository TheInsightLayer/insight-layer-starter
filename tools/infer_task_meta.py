from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
import json
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4", temperature=0.2)

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
    # Use the new `invoke` method
    response = llm.invoke([HumanMessage(content=prompt.format(task_string=task_string))])

    try:
        result = json.loads(response.content)
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
