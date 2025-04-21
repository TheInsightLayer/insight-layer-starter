
import streamlit as st

st.set_page_config(page_title="Insight Layer: New Insight Sources", layout="wide")
st.title("New Insight Sources")

st.markdown("""
These tools help you add new insights directly from everyday work:

### Smart Capture Options
-  **From File:** Upload a CSV or text file and extract key learnings
-  **From SQL:** Run queries against your database and summarize results
-  **From Notes:** Convert raw meeting notes or brainstorms into reusable insight units

---

###  Use These Tools

👉 [**Add Insight from File**](./8_Add_Insight_From_File)  
👉 [**Add Insight from SQL**](./9_Add_Insight_From_SQL)  
👉 [**Add Insight from Notes**](./10_Add_Insight_From_Notes)

---

You can tag, score, and reuse any insights created from these sources just like agent-generated ones.
""")
