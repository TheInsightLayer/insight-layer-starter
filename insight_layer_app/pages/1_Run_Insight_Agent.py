import sys
import os
import streamlit as st
import time
from datetime import datetime

def wrap_as_insight_unit(task_input: str, result: str, task_meta: dict) -> dict:
    """Wraps a generated insight into the standardized InsightUnit schema."""
    return {
        "schema_version": "v1.1",
        "id": f"auto_{int(time.time())}",
        "title": task_input,
        "status": "active",
        "type": "PromptAnchor",
        "tags": ["agent_generated"],
        "narrative": {
            "who": task_meta.get("requestor", "User"),
            "what": result,
            "why": task_meta.get("reason", "—"),
            "how": task_meta.get("method", "—"),
            "outcome": "Pending evaluation",
            "when": datetime.now().strftime("%Y-%m-%d"),
            "roles": ["copilot_user"],
            "source": "insight_layer_agent",
            "review_status": "draft"
        },
        "confidence": {
            "level": "generated",
            "score": 0.6,
            "linked_outcome": task_meta.get("linked_outcome", "unspecified")
        },
        "fidelity": {
            "level": "initial",
            "match_score": 0.5,
            "validated_on": datetime.now().strftime("%Y-%m-%d"),
            "review_needed": True
        },
        "prompt": {
            "prompt_tags": task_meta.get("tags", []),
            "grounding_phrases": task_meta.get("grounding", [])
        },
        "reuse": {
            "times_referenced": 0,
            "created_by": "copilot",
            "created_at": datetime.now().isoformat(),
            "last_updated_by": "copilot",
            "expiration_date": None
        },
        "audience_profiles": ["insight_layer_user"],
        "business_context": {
            "division": "AI Ops",
            "region": "Global"
        },
        "access_control": {
            "visibility": "internal",
            "allowed_roles": ["data_analyst", "ai_user"]
        },
        "security_classification": "internal",
        "confidentiality": "team_only"
    }

def main():
    # Add src to path inside main — Streamlit honors this better
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    SRC_PATH = os.path.join(PROJECT_ROOT, "src")
    if SRC_PATH not in sys.path:
        sys.path.insert(0, SRC_PATH)

    # Imports moved here so sys.path is updated first
    from src.graph.task_parser import parse_task
    from src.graph.prompt_constructor import construct_prompt
    from src.memory.summarizer import summarize_and_normalize
    from src.graph.task_agent import run_task
    from src.memory.insight_layer_memory import InsightLayerMemory

    st.set_page_config(page_title="Insight Layer: Run Task", layout="wide")
    st.title("Run Insight Agent")

    memory = InsightLayerMemory(vault_path="data/memory.db")
    task_input = st.text_input("What do you want the agent to do?", "Create a Q3 customer retention strategy")

    if st.button("Run Agent"):
        task_meta = parse_task(task_input)
        context = memory.load_context(task_meta)
        enriched_prompt = construct_prompt(task_input, context, purpose=task_meta.get("purpose", "general"))

        result = run_task(enriched_prompt, task_meta)
        # summary = summarize_and_normalize(result, task_meta)  # replaced

        # ✅ Updated to InsightUnit schema
        summary = wrap_as_insight_unit(task_input, result, task_meta)
        summary["prompt_style"] = "default"
        summary["prompt_template"] = "basic_v1"

        st.success("Agent run complete.")
        st.subheader("Result:")
        st.write(result)
        st.subheader("New Insight Stored:")
        st.json(summary)

        feedback = st.radio("Was this output helpful?", ["👍 Yes", "👎 No", "🟡 Neutral"], key="feedback")
        if st.button("Submit Feedback"):
            summary["user_feedback"] = feedback
            memory.save_context(summary)
            st.success("✅ Feedback saved.")

if __name__ == "__main__":
    main()
