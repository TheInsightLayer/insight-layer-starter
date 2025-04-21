
# --- 1_Run_Insight_Agent.py ---
import streamlit as st
from src.graph.task_parser import parse_task
from src.graph.prompt_constructor import construct_prompt
from src.graph.summarizer import summarize_output
from src.graph.task_agent import run_task
from src.memory.insight_layer_memory import InsightLayerMemory

def main():
    st.set_page_config(page_title="Insight Layer: Run Task", layout="wide")
    st.title("Run Insight Agent")

    memory = InsightLayerMemory(vault_path="data/memory.db")
    task_input = st.text_input("What do you want the agent to do?", "Create a Q3 customer retention strategy")

    if st.button("Run Agent"):
        task_meta = parse_task(task_input)
        context = memory.load_context(task_meta)
        enriched_prompt = construct_prompt(task_input, context, purpose=task_meta.get("purpose", "general"))

        result = run_task(enriched_prompt, task_meta)
        summary = summarize_output(result, task_meta)
        summary["prompt_style"] = "default"
        summary["prompt_template"] = "basic_v1"

        st.success("Agent run complete.")
        st.subheader("Result:")
        st.write(result)
        st.subheader("New Insight Stored:")
        st.json(summary)

        feedback = st.radio("Was this output helpful?", ["👍 Yes", "👎 No", "🟡 Neutral"], key="feedback")
        if st.button("Submit Feedback"):
            summary["user_feedback"] = feedback
            memory.save_context(summary)
            st.success("✅ Feedback saved.")

if __name__ == "__main__":
    main()
