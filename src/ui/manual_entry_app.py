import streamlit as st
import json
from datetime import datetime
from src.storage.insight_store import save_insights
from src.storage.embedding_store import embed_insights
from src.utils.audit_log import log_event

INSIGHT_JSON_PATH = "data/insights.json"

def load_insights():
    with open(INSIGHT_JSON_PATH) as f:
        return json.load(f)

def save_all_insights(new_item):
    log_event("created", new_item)
    insights = load_insights()
    insights.append(new_item)
    with open(INSIGHT_JSON_PATH, "w") as f:
        json.dump(insights, f, indent=2)
    save_insights([new_item])
    embed_insights(insights)

st.title("Manually Add Insight")

with st.form("manual_form"):
    insight = st.text_area("Insight")
    tags = st.text_input("Tags (comma-separated)")
    related_to = st.text_input("Related Topics (comma-separated)")
    source = st.text_input("Source File", value="manual-entry.txt")
    submitted = st.form_submit_button("Add Insight")

    if submitted and insight:
        new_item = {
            "source": source,
            "insight": insight,
            "tags": [tag.strip() for tag in tags.split(",") if tag],
            "related_to": [r.strip() for r in related_to.split(",") if r],
            "timestamp": datetime.now().isoformat()
        }
        save_all_insights(new_item)
        st.success("✅ Insight added, stored, and embedded!")