import sys
import os
import streamlit as st
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.memory.insight_layer_memory import InsightLayerMemory

memory = InsightLayerMemory()

def main():
    st.set_page_config(page_title="Insight Layer: Bundle Viewer", layout="wide")
    st.title("Insight Bundles by Role")

    role = st.selectbox("Choose your role", ["field_marketer", "engineer", "product_manager"])
    insight_dir = "data/insights"  # or use "data/normalized_insights" if that's where you're storing InsightUnits
    bundle_dir = "data/bundles"

    for fname in os.listdir(bundle_dir):
        if not fname.endswith(".json"):
            continue
        try:
            with open(os.path.join(bundle_dir, fname)) as f:
                bundle = json.load(f)
        except Exception as e:
            st.warning(f"Could not read bundle {fname}: {e}")
            continue

        if bundle.get("role") != role:
            continue

        st.subheader(bundle.get("name", "Unnamed Bundle"))
        st.write(bundle.get("summary", ""))

        for iid in bundle.get("insights", []):
            ipath = os.path.join(insight_dir, f"{iid}.json")
            if not os.path.exists(ipath):
                st.warning(f"Missing insight: {iid}")
                continue

            try:
                with open(ipath) as inf:
                    insight = json.load(inf)
            except json.JSONDecodeError:
                st.error(f"Invalid JSON in {iid}")
                continue

            narr = insight.get("narrative", {})
            title = narr.get("what", f"Insight {iid}")
            with st.expander(f"{title}"):
                st.markdown(f"**Why:** {narr.get('why', '—')}")
                st.markdown(f"**Outcome:** {narr.get('outcome', '—')}")
                st.markdown(f"**When:** {narr.get('when', '—')}")
                st.markdown(f"**Source:** {narr.get('source', '—')}")

                if st.button(f"View {iid}"):
                    memory.increment_usage(iid)
                    st.success(f"Viewing insight: {title}")

if __name__ == "__main__":
    main()
