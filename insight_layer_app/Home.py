
import streamlit as st
from dotenv import load_dotenv
load_dotenv()


st.set_page_config(page_title="Insight Layer Hub", layout="wide")
st.title("Insight Layer: Memory as Infrastructure")

st.markdown("""
Welcome to the Insight Layer.

This tool helps you **capture, score, and reuse** the insights that matter most across roles, teams, and time.

Use the sidebar to access:
- Agent task memory tools
- Role-based onboarding insight packs
- Admin tools for managing bundles
- Visualization and scoring interfaces
- Grounding and validation utilities
""")
