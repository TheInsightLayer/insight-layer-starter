import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import os
import json
from src.graph.grounding_tool import check_watch_sources



def main():
    st.set_page_config(page_title="Insight Layer: Grounding Validator", layout="wide")
    st.title("Check Insight Grounding")

    insight_dir = "data/insights"
    fname = st.selectbox(
        "Choose an insight file",
        [f for f in os.listdir(insight_dir) if f.endswith(".json")]
    )

    with open(os.path.join(insight_dir, fname)) as f:
        insight = json.load(f)

    st.subheader(insight.get("what"))
    st.markdown(f"**Why:** {insight.get('why')}")
    st.markdown(f"**Outcome:** {insight.get('outcome')}")
    st.markdown("---")

    results = check_watch_sources(insight)
    for r in results:
        st.markdown(f"- {r}")

if __name__ == "__main__":
    main()
