
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from src.graph.summarizer import summarize_output
from src.memory.insight_layer_memory import InsightLayerMemory

def main():
    st.set_page_config(page_title="Insight Layer: Add Insight From File", layout="wide")
    st.title("Add Insight From File or Table")

    uploaded_file = st.file_uploader("Upload a CSV or Markdown file", type=["csv", "md", "txt"])

    if uploaded_file:
        file_ext = uploaded_file.name.split('.')[-1]
        content = ""

        if file_ext == "csv":
            df = pd.read_csv(uploaded_file)
            st.subheader("Parsed Data")
            st.dataframe(df.head())
            content = df.to_markdown(index=False)
        else:
            content = uploaded_file.read().decode("utf-8")
            st.subheader("File Content")
            st.code(content[:1000])  # truncate preview

        st.markdown("---")
        st.subheader("Generate Insight")
        user_purpose = st.text_input("What is the purpose of this file?", "Example: detect churn spike")
        user_topic = st.text_input("Topic area", "Example: retention")
        user_quarter = st.text_input("Quarter or timeframe", "Q2")

        if st.button("Generate Insight from File"):
            task_meta = {
                "purpose": user_purpose,
                "topic": user_topic,
                "quarter": user_quarter
            }
            generated = summarize_output(content, task_meta)

            st.success("Insight generated. You can now edit and confirm it below:")
            st.json(generated)

            if st.button("Save Insight"):
                memory = InsightLayerMemory()
                memory.save_context(generated)
                st.success("Insight saved!")

if __name__ == "__main__":
    main()
