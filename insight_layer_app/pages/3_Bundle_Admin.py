import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import json



def main():
    st.set_page_config(page_title="Insight Layer: Bundle Admin", layout="wide")
    st.title("Manage Insight Bundles")

    insight_dir = "data/insights"
    bundle_dir = "data/bundles"
    os.makedirs(bundle_dir, exist_ok=True)

    bundle_id = st.text_input("Bundle ID", "new_bundle")
    name = st.text_input("Bundle Name")
    role = st.selectbox("Role", ["field_marketer", "engineer", "product_manager"])
    summary = st.text_area("Summary")
    selected = []

    candidates = []
    for f in os.listdir(insight_dir):
        if f.endswith(".json"):
            with open(os.path.join(insight_dir, f)) as j:
                d = json.load(j)
                if role in d.get("roles", []):
                    candidates.append((f.replace(".json", ""), d["what"]))

    selected = st.multiselect(
        "Select insights",
        [c[0] for c in candidates],
        format_func=lambda x: next(c[1] for c in candidates if c[0] == x)
    )

    if st.button("Save Bundle"):
        out = {
            "bundle_id": bundle_id,
            "name": name,
            "role": role,
            "summary": summary,
            "insights": selected
        }
        with open(os.path.join(bundle_dir, f"{bundle_id}.json"), "w") as f:
            json.dump(out, f, indent=2)
        st.success("Bundle saved!")

if __name__ == "__main__":
    main()
