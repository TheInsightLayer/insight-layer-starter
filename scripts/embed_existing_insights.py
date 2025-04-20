import json
from src.storage.embedding_store import embed_insights

with open("data/insights.json") as f:
    insights = json.load(f)

embed_insights(insights)