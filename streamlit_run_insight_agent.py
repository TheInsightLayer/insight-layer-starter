import streamlit as st
import os
import yaml
from src.graph.task_parser import parse_task
from src.graph.dynamic_prompt_builder import build_dynamic_prompt
from src.graph.task_agent import run_task
from src.graph.summarizer import summarize_output
from src.memory.insight_layer_memory import InsightLayerMemory
from agents.insight_layer_langgraph_full_agent import insight_agent_graph
from tools.infer_task_meta_with_threshold import infer_task_meta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
CONFIG_PATH = os.getenv("INSIGHT_AGENT_CONFIG", "configs/insight_agent_config.yaml")

st.set_page_config(page_title="Insight Layer: Run Agent", layout="wide")
st.title(" Run Insight Agent")

mode = st.radio("Choose run mode", [" Freeform Prompt", " Config-Driven (LangGraph)"])

if mode == " Freeform Prompt":
    memory = InsightLayerMemory(vault_path="data/memory.db")

    task_input = st.text_input("What do you want the agent to do?", "Create a Q3 customer retention strategy")

    if st.button("Run Freeform Agent"):
        task_meta = parse_task(task_input)
        context = memory.load_context(task_meta)
        enriched_prompt = build_dynamic_prompt(task_input, context, task_meta)
        result = run_task(enriched_prompt, task_meta)
        summary = summarize_output(result, task_meta)
        memory.save_context(summary)

        st.success(" Agent run complete!")
        st.subheader(" Output:")
        st.write(result)
        st.subheader(" Insight Stored:")
        st.json(summary)

else:
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    st.text_area("Task", value=config.get("task", ""), key="task_text", height=100)
    config["task"] = st.session_state["task_text"]

    if "task_meta" not in config or not config["task_meta"]:
        st.warning("No metadata found — ready to infer from task.")
        if st.button(" Auto-Infer Metadata"):
            inferred = infer_task_meta(config["task"])
            config["task_meta"] = inferred
            st.success(" Metadata Inferred!")
            st.json(inferred)

    if st.button(" Run Config Agent"):
        result = insight_agent_graph.invoke(config)
        st.success(" Agent finished!")

        st.subheader(" Output:")
        st.write(result["agent_output"])
        st.subheader(" Insight Saved:")
        st.json(result["saved_insight"])

        if result.get("bundle_updated"):
            st.subheader(" Bundle Updated:")
            st.write(result["bundle_updated"])
