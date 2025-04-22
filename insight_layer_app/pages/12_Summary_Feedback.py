import streamlit as st
import os
import json
from datetime import datetime

OUTCOME_LOG_PATH = "data/trace_logs/summary_outcomes"
SUMMARY_DIR = "data/trace_logs/summaries"

os.makedirs(OUTCOME_LOG_PATH, exist_ok=True)
os.makedirs(SUMMARY_DIR, exist_ok=True)

def load_recent_summaries(limit=10):
    files = sorted(os.listdir(SUMMARY_DIR), reverse=True)
    summaries = []
    for f in files[:limit]:
        if f.endswith(".json"):
            with open(os.path.join(SUMMARY_DIR, f)) as j:
                try:
                    data = json.load(j)
                    summaries.append((f, data))
                except json.JSONDecodeError:
                    continue
    return summaries

def log_feedback(summary_id, feedback):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_entry = {
        "summary_id": summary_id,
        "feedback": feedback,
        "logged_at": timestamp
    }
    fname = f"feedback_{summary_id}_{timestamp}.json"
    with open(os.path.join(OUTCOME_LOG_PATH, fname), "w") as f:
        json.dump(log_entry, f, indent=2)

def main():
    st.set_page_config(page_title="Insight Layer: Feedback Tracker", layout="wide")
    st.title("✅ Insight Summary Feedback")

    summaries = load_recent_summaries()

    if not summaries:
        st.info("No recent summaries found.")
        return

    for filename, data in summaries:
        insight = data.get("summary", {})
        st.subheader(insight.get("what", "No Title"))
        st.markdown(f"**Why:** {insight.get('why', '—')}  
**Outcome:** {insight.get('outcome', '—')}")
        st.markdown(f"**Source:** {insight.get('source', '—')}")

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("👍 Useful", key=f"useful_{filename}"):
                log_feedback(filename, "useful")
                st.success("Feedback saved: Useful ✅")
        with col2:
            if st.button("👎 Not Useful", key=f"not_useful_{filename}"):
                log_feedback(filename, "not_useful")
                st.warning("Feedback saved: Not Useful ❌")

if __name__ == "__main__":
    main()
