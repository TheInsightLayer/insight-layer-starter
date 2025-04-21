import os
import json
import pytest
from src.utils.insight_pusher import InsightPusher

@pytest.fixture
def setup_insights():
    # Create a temporary directory for test insights
    test_dir = "test_insights"
    os.makedirs(test_dir, exist_ok=True)

    # Create test insights
    insights = [
        {
            "id": "insight_1",
            "what": "Insight for engineers",
            "roles": ["engineer"],
            "review_status": "approved",
            "when": "2023-03-01",
            "importance_score": 9.0
        },
        {
            "id": "insight_2",
            "what": "Insight for product managers",
            "roles": ["product_manager"],
            "review_status": "approved",
            "when": "2022-01-01",
            "importance_score": 7.5
        },
        {
            "id": "insight_3",
            "what": "Old insight for engineers",
            "roles": ["engineer"],
            "review_status": "approved",
            "when": "2020-01-01",
            "importance_score": 6.0
        }
    ]

    for insight in insights:
        with open(os.path.join(test_dir, f"{insight['id']}.json"), "w") as f:
            json.dump(insight, f)

    yield test_dir

    # Cleanup after test
    for fname in os.listdir(test_dir):
        os.remove(os.path.join(test_dir, fname))
    os.rmdir(test_dir)

def test_recommend_insights(setup_insights, monkeypatch):
    # Monkeypatch the insight directory
    pusher = InsightPusher()
    monkeypatch.setattr(pusher.memory, "insight_dir", setup_insights)

    # Test recommendations for engineers
    recommendations = pusher.recommend_insights(user_role="engineer", max_insights=2)
    assert len(recommendations) == 1
    assert recommendations[0]["id"] == "insight_1"