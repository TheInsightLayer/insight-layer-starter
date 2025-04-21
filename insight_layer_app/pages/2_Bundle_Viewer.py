import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import json
from src.memory.insight_layer_memory import InsightLayerMemory

memory = InsightLayerMemory()

def main():
    st.set_page_config(page_title="Insight Layer: Bundle Viewer", layout="wide")
    st.title("Insight Bundles by Role")

    role = st.selectbox("Choose your role", ["field_marketer", "engineer", "product_manager"])
    insight_dir = "data/insights"
    bundle_dir = "data/bundles"

    for fname in os.listdir(bundle_dir):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(bundle_dir, fname)) as f:
            bundle = json.load(f)
            if bundle["role"] != role:
                continue
            st.subheader(bundle["name"])
            st.write(bundle["summary"])
            for iid in bundle["insights"]:
                ipath = os.path.join(insight_dir, f"{iid}.json")
                if os.path.exists(ipath):
                    with open(ipath) as inf:
                        insight = json.load(inf)
                        with st.expander(f"{insight['what']}"):
                            st.write(insight.get("why"))
                            st.write(insight.get("outcome"))
                            if st.button(f"View {insight['id']}"):
                                memory.increment_usage(insight["id"])
                                st.write(f"Viewing insight: {insight['what']}")

if __name__ == "__main__":
    main()
