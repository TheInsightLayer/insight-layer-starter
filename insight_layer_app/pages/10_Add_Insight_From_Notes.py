
import streamlit as st
import os
import json
from datetime import datetime
from src.graph.summarizer import summarize_output
from src.memory.insight_layer_memory import InsightLayerMemory

def main():
    st.set_page_config(page_title="Insight Layer: Add Insight From Notes", layout="wide")
    st.title("Add Insight From Meeting Notes or Text")

    raw_notes = st.text_area("Paste raw meeting notes, email threads, or brainstorming text")

    user_purpose = st.text_input("Purpose", "decision making")
    user_topic = st.text_input("Topic", "launch planning")
    user_quarter = st.text_input("Timeframe", "Q3")

    if st.button("Generate Insight"):
        task_meta = {
            "purpose": user_purpose,
            "topic": user_topic,
            "quarter": user_quarter
        }

        generated = summarize_output(raw_notes, task_meta)

        st.success("Insight generated from notes. You can now edit and save it.")
        st.json(generated)

        if st.button("Save Insight"):
            memory = InsightLayerMemory()
            memory.save_context(generated)
            st.success("Insight saved!")

if __name__ == "__main__":
    main()
