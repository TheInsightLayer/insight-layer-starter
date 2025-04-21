
import os
import json
from src.utils.review_classifier import auto_score_review

def review_unscored_insights(directory="data/insights"):
    for fname in os.listdir(directory):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(directory, fname)
        with open(fpath, "r") as f:
            insight = json.load(f)

        if "review_status" not in insight or insight["review_status"] == "pending":
            review = auto_score_review(insight)
            insight.update(review)
            with open(fpath, "w") as f:
                json.dump(insight, f, indent=2)
            print(f"✅ Reviewed: {fname}")
