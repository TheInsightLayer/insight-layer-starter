import sys
import os
import streamlit as st
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

def main():
    st.set_page_config(page_title="Insight Layer: Onboarding", layout="wide")
    st.title("Onboarding Insight Pack")

    insight_dir = "data/insights"  # Or "data/normalized_insights"
    user = st.text_input("Your name (to track progress):", "new_user")
    role = st.selectbox("Your role:", ["engineer", "field_marketer", "product_manager"])

    track_file = "data/user_completion.json"
    if not os.path.exists(track_file):
        with open(track_file, "w") as f:
            json.dump({}, f)

    with open(track_file, "r") as f:
        user_data = json.load(f)
    user_data.setdefault(user, {})

    matched = []
    for f in os.listdir(insight_dir):
        if f.endswith(".json"):
            try:
                with open(os.path.join(insight_dir, f)) as j:
                    d = json.load(j)
                    narr = d.get("narrative", {})
                    if role in narr.get("roles", []) and narr.get("review_status") in ["approved", "auto"]:
                        matched.append((f, narr))
            except Exception as e:
                st.warning(f"Skipping {f}: {e}")

    for fname, narr in matched:
        with st.expander(f"{narr.get('what', fname)} — {narr.get('badge', '')}"):
            st.markdown(
                f"**Why:** {narr.get('why', '—')}  \n**Outcome:** {narr.get('outcome', '—')}"
            )
            if user_data[user].get(fname):
                st.markdown("✅ Already read")
            else:
                if st.button(f"Mark as read: {fname}", key=f"{user}-{fname}"):
                    user_data[user][fname] = True
                    with open(track_file, "w") as f:
                        json.dump(user_data, f, indent=2)
                    st.success("✅ Marked as read!")

if __name__ == "__main__":
    main()
