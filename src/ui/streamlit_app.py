import streamlit as st
import json
import pandas as pd
from datetime import datetime
from src.storage.embedding_store import search_insights as semantic_search, update_embedding, embed_insights
from src.storage.insight_store import search_insights as keyword_search, save_insights, replace_insight
from src.utils.insight_pipeline import extract_insights
from src.utils.audit_log import log_event

INSIGHT_JSON_PATH = "data/insights.json"

def load_insights():
    with open(INSIGHT_JSON_PATH) as f:
        return json.load(f)

def save_all_insights(new_item):
    log_event("created", new_item)
    insights = load_insights()
    insights.append(new_item)
    with open(INSIGHT_JSON_PATH, "w") as f:
        json.dump(insights, f, indent=2)
    save_insights([new_item])
    embed_insights(insights)

def export_to_csv(data):
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode("utf-8")

# Layout
st.title("Insight Layer")
st.markdown("""
Welcome to the Insight Layer! 👋  
Use the sidebar to search for insights extracted from your documentation.

- Use **Keyword** for exact text search  
- Use **Semantic** to find related ideas (embedding required)  
- Click 🔁 to re-extract insights using the latest model  
- Use the **Manual Entry** tab to add your own insights  
- Export your findings with the 📤 button  
""")
tab1, tab2 = st.tabs(["Search & Re-extract", "Manual Entry"])

# Tab 1: Search & Re-extract
with tab1:
    st.sidebar.header("🔎 Search Insights")
    search_mode = st.sidebar.radio("Search mode", ["Keyword", "Semantic (Embedding)"])
    query = st.sidebar.text_input("Enter search text", placeholder="Try roles, alignment, checklists...")
    search_trigger = st.sidebar.button("Search")

    all_insights = load_insights()
    results = []

    if search_trigger and query:
        if search_mode == "Keyword":
            results = keyword_search(keyword=query)
        else:
            results = semantic_search(query)

    if results:
        st.markdown(f"### Found {len(results)} insight(s):")

        exportable = []
        for i, row in enumerate(results):
            if isinstance(row, tuple):
                row_id, source, insight, tags, related_to, timestamp = row
                metadata = {
                    "source": source,
                    "insight": insight,
                    "tags": tags.split(", "),
                    "related_to": related_to.split(", "),
                    "timestamp": timestamp
                }
            else:
                row_id = i
                metadata = row

            exportable.append(metadata)

            st.markdown(f"**Insight:** {metadata['insight']}")
            st.markdown(f"*Tags:* {', '.join(metadata.get('tags', []))}")
            st.markdown(f"*Source:* {metadata.get('source')}  \n*Time:* {metadata.get('timestamp')}")
            st.markdown("---")

            if st.button("🔁 Re-extract", key=f"rextract_{i}"):
                updated = extract_insights(metadata["insight"])
                if updated:
                    updated[0]["source"] = metadata["source"]
                    all_insights[row_id] = updated[0]
                    with open(INSIGHT_JSON_PATH, "w") as f:
                        json.dump(all_insights, f, indent=2)
                    replace_insight(row_id + 1, updated[0])  # SQLite ID is 1-based
                    update_embedding(row_id, updated[0])
                    log_event("reextracted", updated[0])
                    st.success("Insight re-extracted, updated in DB, and re-embedded!")
                    st.rerun()

        csv_data = export_to_csv(exportable)
        st.download_button("📤Download CSV", csv_data, file_name="insights_export.csv", mime="text/csv")
    else:
        st.info("Enter a query to search insights.")

# Tab 2: Manual Insight Entry
with tab2:
    with st.form("manual_form"):
        insight = st.text_area("Insight")
        tags = st.text_input("Tags (comma-separated)")
        related_to = st.text_input("Related Topics (comma-separated)")
        source = st.text_input("Source File", value="manual-entry.txt")
        submitted = st.form_submit_button("Add Insight")

        if submitted and insight:
            new_item = {
                "source": source,
                "insight": insight,
                "tags": [tag.strip() for tag in tags.split(",") if tag],
                "related_to": [r.strip() for r in related_to.split(",") if r],
                "timestamp": datetime.now().isoformat()
            }
            save_all_insights(new_item)
            st.success("Insight added, stored, and embedded!")