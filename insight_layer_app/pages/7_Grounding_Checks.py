import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import json
from src.graph.grounding_tool import check_watch_sources

def main():
    st.set_page_config(page_title="Insight Layer: Grounding Validator", layout="wide")
    st.title("Check Insight Grounding")

    insight_dir = "data/insights"  # Or "data/normalized_insights"
    fname = st.selectbox(
        "Choose an insight file",
        [f for f in os.listdir(insight_dir) if f.endswith(".json")]
    )

    with open(os.path.join(insight_dir, fname)) as f:
        insight = json.load(f)

    narr = insight.get("narrative", {})

    st.subheader(narr.get("what", "Untitled Insight"))
    st.markdown(f"**Why:** {narr.get('why', '—')}")
    st.markdown(f"**Outcome:** {narr.get('outcome', '—')}")
    st.markdown("---")

    results = check_watch_sources(insight)  # Make sure this function handles InsightUnit structure
    if results:
        for r in results:
            st.markdown(f"- {r}")
    else:
        st.success("✅ All watch sources appear valid or were not found.")

if __name__ == "__main__":
    main()
