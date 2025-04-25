# src/graph/run_task_with_trace.py

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

PROMPT_TRACE_PATH = "data/trace_logs/prompts"
os.makedirs(PROMPT_TRACE_PATH, exist_ok=True)

# Initialize LLM client
client = ChatOpenAI(
    model="gpt-4",
    temperature=0.3,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def log_prompt_trace(
    task: str,
    task_meta: Dict,
    insights: List[Dict],
    prompt: str,
    output: str,
    success: bool
):
    """
    Records a full trace of each prompt execution for monitoring and reuse analysis.
    """
    trace = {
        "task": task,
        "task_meta": task_meta,
        "used_insights": insights,
        "prompt": prompt,
        "output": output,
        "success": success,
        "timestamp": datetime.now().isoformat()
    }
    filename = f"prompt_trace_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    with open(os.path.join(PROMPT_TRACE_PATH, filename), "w") as f:
        json.dump(trace, f, indent=2)

def run_task(
    prompt: str,
    task_meta: Optional[Dict] = None,
    insights: Optional[List[Dict]] = None
) -> str:
    """
    Executes a system + human prompt with optional metadata and insights context.

    Logs the interaction for reproducibility and prompt performance analysis.
    """
    task_meta = task_meta or {}
    insights = insights or []

    system_msg = SystemMessage(content=f"You are an assistant specializing in {task_meta.get('purpose', 'general')}.")

    try:
        response = client.invoke([
            system_msg,
            HumanMessage(content=prompt)
        ])
        output = response.content.strip()
        log_prompt_trace(
            task=task_meta.get("task", prompt),
            task_meta=task_meta,
            insights=insights,
            prompt=prompt,
            output=output,
            success=True
        )
        return output

    except Exception as e:
        error_message = str(e)
        log_prompt_trace(
            task=task_meta.get("task", prompt),
            task_meta=task_meta,
            insights=insights,
            prompt=prompt,
            output=error_message,
            success=False
        )
        raise RuntimeError(f"Prompt execution failed: {error_message}")
