import sys
import os
import time
import json
import pandas as pd
from datetime import datetime
import streamlit as st

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.memory.insight_layer_memory import InsightLayerMemory

def wrap_as_insight_unit_from_text(content: str, task_meta: dict) -> dict:
    """Wrap plain file content and metadata into an InsightUnit structure."""
    return {
        "schema_version": "v1.1",
        "id": f"auto_{int(time.time())}",
        "title": f"{task_meta.get('topic', 'Untitled')} - {task_meta.get('quarter', '')}",
        "status": "active",
        "type": "FileGenerated",
        "tags": [task_meta.get("topic", "insight")],
        "narrative": {
            "what": content[:300] + "...",
            "why": task_meta.get("purpose", "—"),
            "how": "Generated from uploaded file",
            "outcome": "Pending evaluation",
            "when": datetime.now().strftime("%Y-%m-%d"),
            "roles": ["analyst"],
            "source": "file_upload",
            "review_status": "draft"
        },
        "confidence": {
            "level": "generated",
            "score": 0.4
        },
        "fidelity": {
            "level": "low",
            "match_score": 0.3,
            "review_needed": True
        },
        "reuse": {
            "times_referenced": 0,
            "created_by": "file_uploader",
            "created_at": datetime.now().isoformat(),
            "last_updated_by": "file_uploader"
        },
        "audience_profiles": ["onboarding_user"],
        "business_context": {
            "division": "Insights",
            "region": "Global"
        },
        "access_control": {
            "visibility": "internal",
            "allowed_roles": ["analyst"]
        },
        "security_classification": "internal",
        "confidentiality": "team_only"
    }

def main():
    st.set_page_config(page_title="Insight Layer: Add Insight From File", layout="wide")
    st.title("Add Insight From File or Table")

    uploaded_file = st.file_uploader("Upload a CSV or Markdown file", type=["csv", "md", "txt"])

    content = ""
    if uploaded_file:
        file_ext = uploaded_file.name.split('.')[-1]

        if file_ext == "csv":
            df = pd.read_csv(uploaded_file)
            st.subheader("Parsed Data")
            st.dataframe(df.head())
            content = df.to_markdown(index=False)
        else:
            content = uploaded_file.read().decode("utf-8")
            st.subheader("File Content")
            st.code(content[:1000])  # Preview first 1000 characters

    if content:
        st.markdown("---")
        st.subheader("Generate Insight")
        user_purpose = st.text_input("What is the purpose of this file?", "Example: detect churn spike")
        user_topic = st.text_input("Topic area", "Example: retention")
        user_quarter = st.text_input("Quarter or timeframe", "Q2")

        if st.button("Generate Insight from File"):
            task_meta = {
                "purpose": user_purpose,
                "topic": user_topic,
                "quarter": user_quarter
            }
            generated = wrap_as_insight_unit_from_text(content, task_meta)

            st.success("Insight generated. You can now edit and confirm it below:")
            st.json(generated)

            if st.button("Save Insight"):
                memory = InsightLayerMemory()
                memory.save_context(generated)
                st.success("Insight saved!")

if __name__ == "__main__":
    main()
