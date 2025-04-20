from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatOpenAI(model="gpt-4", temperature=0.3, api_key=os.getenv("OPENAI_API_KEY"))

extract_prompt = ChatPromptTemplate.from_template("""
You are an assistant that extracts reusable insights from business documentation.

Instructions:
- Return a list of 1–3 insights in valid JSON format.
- Each insight must include:
  - "insight": a concise, reusable takeaway
  - "tags": a list of keywords
  - "related_to": a list of related concepts (can be empty)
  - "source": set this to "{source}"
  - "timestamp": set to the current time

TEXT:
{text}
""")

extract_chain = extract_prompt | get_llm()

def extract_insights(text, source="example-guide.txt"):
    try:
        result = extract_chain.invoke({"text": text, "source": source})
        insights = eval(result.content)  # expects JSON-style list
    except Exception as e:
        insights = [{
            "source": source,
            "insight": f"Error parsing model output: {e}",
            "tags": ["error"],
            "related_to": [],
            "timestamp": datetime.now().isoformat()
        }]
    return insights