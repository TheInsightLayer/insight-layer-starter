#!/bin/bash
echo "Activating virtual environment..."
source .venv/bin/activate

echo "Launching Insight Layer Streamlit UI..."
streamlit run src/ui/streamlit_app.py