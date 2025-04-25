import sys
import os
import json
from datetime import datetime
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

OUTCOME_LOG_PATH = "data/trace_logs/summary_outcomes"
SUMMARY_DIR = "data/trace_logs/summaries"

os.makedirs(OUTCOME_LOG_PATH, exist_ok=True)
os.makedirs(SUMMARY_DIR, exist_ok=True)

def load_recent_summaries(limit=10):
    files = sorted(os.listdir(SUMMARY_DIR), reverse=True)
    summaries = []
    for f in files[:limit]:
        if f.endswith(".json"):
            try:
                with open(os.path.join(SUMMARY_DIR, f)) as j:
                    data = json.load(j)
                    # If summary is nested, extract it
                    insight = data.get("summary", data)  # fallback to root if no "summary"
                    summaries.append((f, insight))
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
    st.title("Insight Summary Feedback")

    summaries = load_recent_summaries()

    if not summaries:
        st.info("No recent summaries found.")
        return

    for filename, summary in summaries:
        narr = summary.get("narrative", {})
        st.subheader(narr.get("what", "No Title"))
        st.markdown(f"**Why:** {narr.get('why', '—')}  \n**Outcome:** {narr.get('outcome', '—')}")
        st.markdown(f"**Source:** {narr.get('source', '—')}")

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("👍 Useful", key=f"useful_{filename}"):
                log_feedback(filename, "useful")
                st.success("Feedback saved: Useful")
        with col2:
            if st.button("👎 Not Useful", key=f"not_useful_{filename}"):
                log_feedback(filename, "not_useful")
                st.warning("Feedback saved: Not Useful")

if __name__ == "__main__":
    main()
