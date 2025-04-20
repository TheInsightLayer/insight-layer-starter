from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
import json
from datetime import datetime
from src.utils.audit_log import log_event
from src.storage.insight_store import save_insights, search_insights
from src.utils.insight_pipeline import extract_insights

INSIGHT_JSON_PATH = "data/insights.json"

app = FastAPI(title="Insight Layer API")

class Insight(BaseModel):
    insight: str
    tags: List[str]
    related_to: Optional[List[str]] = []
    source: str = "api-entry.txt"
    timestamp: Optional[str] = None

def load_insights():
    with open(INSIGHT_JSON_PATH) as f:
        return json.load(f)

def save_all_insights(new_item):
    insights = load_insights()
    insights.append(new_item)
    with open(INSIGHT_JSON_PATH, "w") as f:
        json.dump(insights, f, indent=2)
    save_insights([new_item])

@app.get("/insights")
def get_insights(keyword: Optional[str] = Query(None), tag: Optional[str] = Query(None)):
    results = search_insights(keyword=keyword, tag=tag)
    insights = []
    for row in results:
        _, source, insight, tags, related_to, timestamp = row
        insights.append({
            "source": source,
            "insight": insight,
            "tags": tags.split(", "),
            "related_to": related_to.split(", "),
            "timestamp": timestamp
        })
    return insights

@app.post("/insights")
def add_insight(item: Insight):
    item.timestamp = datetime.now().isoformat()
    new_item = item.dict()
    save_all_insights(new_item)
    log_event("created", new_item)
    return {"status": "success", "insight": new_item}

@app.post("/extract")
def extract(text: str, source: Optional[str] = "api-extracted.txt"):
    insights = extract_insights(text, source)
    save_all_insights(insights[0])
    log_event("extracted", insights[0])
    return {"status": "success", "insight": insights[0]}