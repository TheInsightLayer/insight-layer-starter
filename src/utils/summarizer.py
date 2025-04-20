from datetime import datetime
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import JsonOutputKeyToolsParser

def extract_insights(text):
    llm = ChatOpenAI(
    model="gpt-4-turbo",
    temperature=0.3,
    api_key=os.getenv("OPENAI_API_KEY")
    )

    prompt = ChatPromptTemplate.from_template("""
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


    formatted_prompt = prompt.format_messages(text=text)
    output = llm(formatted_prompt)
    parsed = JsonOutputKeyToolsParser().parse(output.content)

    return parsed