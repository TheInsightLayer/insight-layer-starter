import json
import sys
from src.utils.insight_pipeline import extract_insights
from src.storage.insight_store import init_db, save_insights

# Initialize DB
init_db()

if "--test" in sys.argv:
    print("Running in test mode with hardcoded text...\n")
    text = "This is a simple test input about how clear documentation improves team alignment during onboarding."
else:
    with open("data/raw_text.txt") as f:
        text = f.read()

insights = extract_insights(text)

# Save to SQLite
save_insights(insights)

# Save to JSON
with open("data/insights.json", "w") as f:
    json.dump(insights, f, indent=2)

print(f"Extracted {len(insights)} insight(s)")
