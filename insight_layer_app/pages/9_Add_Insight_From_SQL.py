
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from src.graph.summarizer import summarize_output
from src.memory.insight_layer_memory import InsightLayerMemory
import sqlite3  # or swap to another engine

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

            generated = summarize_output(content, task_meta)

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
