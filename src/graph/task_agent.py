import os
import json
from datetime import datetime
from openai import OpenAI

PROMPT_TRACE_PATH = "data/trace_logs/prompts"
os.makedirs(PROMPT_TRACE_PATH, exist_ok=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def log_prompt_trace(task: str, task_meta: dict, insights: list, prompt: str, output: str, success: bool):
    """
    Records a full trace of each prompt run — to learn what works over time.
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
    filename = os.path.join(PROMPT_TRACE_PATH, f"prompt_trace_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")
    with open(filename, "w") as f:
        json.dump(trace, f, indent=2)

def run_task(prompt: str, task_meta: dict = None, insights: list = None) -> str:
    """
    Executes the agent prompt with context, records the full trace, and returns the LLM output.
    """
    task_meta = task_meta or {}
    insights = insights or []

    system_msg = f"You are an assistant specializing in {task_meta.get('purpose', 'general')}."
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ]
        )
        output = response.choices[0].message.content.strip()
        log_prompt_trace(task_meta.get("task", prompt), task_meta, insights, prompt, output, success=True)
        return output

    except Exception as e:
        error_message = str(e)
        log_prompt_trace(task_meta.get("task", prompt), task_meta, insights, prompt, error_message, success=False)
        raise e
