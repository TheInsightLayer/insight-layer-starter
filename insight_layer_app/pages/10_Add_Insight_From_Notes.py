import sys
import os
import time
import json
from datetime import datetime
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.memory.insight_layer_memory import InsightLayerMemory

def wrap_as_insight_unit_from_notes(content: str, task_meta: dict) -> dict:
    """Wrap meeting notes or freeform text into a full InsightUnit."""
    return {
        "schema_version": "v1.1",
        "id": f"note_{int(time.time())}",
        "title": f"{task_meta.get('topic', 'Insight')} - {task_meta.get('quarter', '')}",
        "status": "active",
        "type": "MeetingNotes",
        "tags": [task_meta.get("topic", "insight")],
        "narrative": {
            "what": content[:300] + "...",
            "why": task_meta.get("purpose", "—"),
            "how": "Summarized from meeting notes or text input",
            "outcome": "Pending review",
            "when": datetime.now().strftime("%Y-%m-%d"),
            "roles": ["collaborator"],
            "source": "meeting_notes",
            "review_status": "draft"
        },
        "confidence": {
            "level": "interpreted",
            "score": 0.5
        },
        "fidelity": {
            "level": "medium",
            "match_score": 0.5,
            "review_needed": True
        },
        "reuse": {
            "times_referenced": 0,
            "created_by": "notes_input",
            "created_at": datetime.now().isoformat(),
            "last_updated_by": "notes_input"
        },
        "audience_profiles": ["strategic_planner"],
        "business_context": {
            "division": "Strategy",
            "region": "Global"
        },
        "access_control": {
            "visibility": "internal",
            "allowed_roles": ["strategist", "leader"]
        },
        "security_classification": "internal",
        "confidentiality": "team_only"
    }

def main():
    st.set_page_config(page_title="Insight Layer: Add Insight From Notes", layout="wide")
    st.title("Add Insight From Meeting Notes or Text")

    raw_notes = st.text_area("Paste raw meeting notes, email threads, or brainstorming text")

    user_purpose = st.text_input("Purpose", "decision making")
    user_topic = st.text_input("Topic", "launch planning")
    user_quarter = st.text_input("Timeframe", "Q3")

    if st.button("Generate Insight"):
        task_meta = {
            "purpose": user_purpose,
            "topic": user_topic,
            "quarter": user_quarter
        }

        generated = wrap_as_insight_unit_from_notes(raw_notes, task_meta)

        st.success("Insight generated from notes. You can now edit and save it.")
        st.json(generated)

        if st.button("Save Insight"):
            memory = InsightLayerMemory()
            memory.save_context(generated)
            st.success("Insight saved!")

if __name__ == "__main__":
    main()
