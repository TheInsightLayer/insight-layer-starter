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
                    content = json.load(j)

                    # Normalize to a list of InsightUnits
                    insights = content if isinstance(content, list) else [content]

                    for d in insights:
                        if not isinstance(d, dict):
                            st.warning(f"Invalid insight in {f}: {type(d)}")
                            continue
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

    insight_dir = "data/normalized_insights"  # updated to cleaned folder
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
        rows = [(score, i) for score, i in rows if role_filter in i.get("narrative", {}).get("roles", [])]

    search_query = st.text_input("Search insights", "")
    if search_query:
        rows = [(score, i) for score, i in rows if search_query.lower() in i.get("narrative", {}).get("what", "").lower()]

    sort_order = st.radio("Sort Order", ["High to Low", "Low to High"], horizontal=True)
    rows = sorted(rows, reverse=(sort_order == "High to Low"))

    for score, insight in rows:
        narr = insight.get("narrative", {})
        st.expander(f"{narr.get('what', 'Untitled')} — Score: {score:.2f}", expanded=False).markdown(
            f"**Why:** {narr.get('why', '—')}  \n"
            f"**Outcome:** {narr.get('outcome', '—')}  \n"
            f"**When:** {narr.get('when', '—')}  \n"
            f"**Source:** {narr.get('source', '—')}  \n"
            f"**Role(s):** {', '.join(narr.get('roles', []))}  \n"
            f"**Badge:** {narr.get('badge', '—')}"
        )

if __name__ == "__main__":
    main()
