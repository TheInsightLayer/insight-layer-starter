import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import json
from src.utils.scoring import compute_importance
from src.utils.config_loader import load_weights, save_weights

def load_and_score_insights(insight_dir, weights):
    rows = []
    for f in os.listdir(insight_dir):
        if f.endswith(".json"):
            try:
                with open(os.path.join(insight_dir, f)) as j:
                    d = json.load(j)
                    score = compute_importance(d, weights)
                    d["importance_score"] = score
                    rows.append((score, d))
            except (json.JSONDecodeError, FileNotFoundError) as e:
                st.error(f"Error processing file {f}: {e}")
    return sorted(rows, reverse=True)

def main():
    st.set_page_config(page_title="Insight Layer: Importance Viewer", layout="wide")
    st.title("Tune Insight Importance")
    st.caption("Interactively tune scoring weights to reprioritize insights based on recency, impact, and usage.")

    insight_dir = "data/insights"
    weights = load_weights()

    with st.sidebar:
        st.subheader("Adjust Scoring Weights")
        weights["used"] = st.slider("Use weight", 0.0, 1.0, weights.get("used", 0.4))
        weights["links"] = st.slider("Links weight", 0.0, 1.0, weights.get("links", 0.3))
        weights["impact"] = st.slider("Impact weight", 0.0, 1.0, weights.get("impact", 0.1))
        weights["outcome"] = st.slider("Outcome weight", 0.0, 1.0, weights.get("outcome", 0.1))
        weights["recency"] = st.slider("Recency weight", 0.0, 1.0, weights.get("recency", 0.1))

        if st.button("Save Weights"):
            save_weights(weights)
            st.success("Weights saved to `configs/importance_weights.yaml`")

        if st.button("Reset Weights"):
            weights = load_weights()
            st.success("Weights reset to default.")

    with st.spinner("Loading and scoring insights..."):
        rows = load_and_score_insights(insight_dir, weights)

    role_filter = st.selectbox("Filter by role", ["All", "engineer", "field_marketer", "product_manager"])
    if role_filter != "All":
        rows = [(score, insight) for score, insight in rows if role_filter in insight.get("roles", [])]

    search_query = st.text_input("Search insights", "")
    if search_query:
        rows = [(score, insight) for score, insight in rows if search_query.lower() in insight["what"].lower()]

    # Add sort order selection
    sort_order = st.radio("Sort Order", ["High to Low", "Low to High"], horizontal=True)
    rows = sorted(rows, reverse=(sort_order == "High to Low"))

    for score, insight in rows:
        with st.expander(f"{insight['what']} — Score: {score:.2f}"):
            st.markdown(
                f"**Why:** {insight['why']}  \n"
                f"**Outcome:** {insight['outcome']}  \n"
                f"**When:** {insight.get('when', '—')}  \n"
                f"**Source:** {insight.get('source', '—')}"
            )
            st.markdown(f"**Role(s):** {', '.join(insight.get('roles', []))}")
            st.markdown(f"**Badge:** {insight.get('badge', '—')}")

if __name__ == "__main__":
    main()
