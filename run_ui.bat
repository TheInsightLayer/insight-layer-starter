@echo off
echo Activating virtual environment...
call .venv\Scripts\activate

echo Launching Insight Layer Streamlit UI...
streamlit run src\ui\streamlit_app.py

pause