import sys
import os
import time
import json
import pandas as pd
import sqlite3
from datetime import datetime
import streamlit as st

# Add root path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.memory.insight_layer_memory import InsightLayerMemory

def wrap_as_insight_unit_from_sql(content: str, task_meta: dict, query: str) -> dict:
    return {
        "schema_version": "v1.1",
        "id": f"sql_{int(time.time())}",
        "title": f"{task_meta.get('topic', 'Untitled')} - {task_meta.get('quarter', '')}",
        "status": "active",
        "type": "SQLQueryInsight",
        "tags": [task_meta.get("topic", "insight")],
        "narrative": {
            "what": content[:300] + "...",
            "why": task_meta.get("purpose", "—"),
            "how": f"Generated from SQL query:\n\n```sql\n{query.strip()}\n```",
            "outcome": "Pending evaluation",
            "when": datetime.now().strftime("%Y-%m-%d"),
            "roles": ["analyst"],
            "source": "sql_query",
            "review_status": "draft"
        },
        "confidence": {
            "level": "generated",
            "score": 0.5
        },
        "fidelity": {
            "level": "medium",
            "match_score": 0.6,
            "review_needed": True
        },
        "reuse": {
            "times_referenced": 0,
            "created_by": "sql_uploader",
            "created_at": datetime.now().isoformat(),
            "last_updated_by": "sql_uploader"
        },
        "audience_profiles": ["sql_consumer"],
        "business_context": {
            "division": "Insights",
            "region": "Global"
        },
        "access_control": {
            "visibility": "internal",
            "allowed_roles": ["analyst"]
        },
        "security_classification": "internal",
        "confidentiality": "team_only"
    }

def main():
    st.set_page_config(page_title="Insight Layer: Add Insight From SQL", layout="wide")
    st.title("Add Insight From SQL Query")

    db_path = st.text_input("Path to SQLite database", "data/example.db")

    query = st.text_area("SQL Query", "SELECT COUNT(*) AS churned_users FROM users WHERE churned = 1")
    user_purpose = st.text_input("Purpose of this insight", "churn analysis")
    user_topic = st.text_input("Topic", "retention")
    user_quarter = st.text_input("Timeframe", "Q2")

    if st.button("Run & Generate Insight"):
        try:
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()

            st.subheader("Query Results")
            st.dataframe(df)

            content = df.to_markdown(index=False)
            task_meta = {
                "purpose": user_purpose,
                "topic": user_topic,
                "quarter": user_quarter
            }

            generated = wrap_as_insight_unit_from_sql(content, task_meta, query)

            st.success("Insight generated. You can now review and save it.")
            st.json(generated)

            if st.button("Save Insight"):
                memory = InsightLayerMemory()
                memory.save_context(generated)
                st.success("Insight saved to memory!")

        except Exception as e:
            st.error(f"SQL error: {e}")

if __name__ == "__main__":
    main()
