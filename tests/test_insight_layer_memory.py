import os
import json
import pytest
from unittest.mock import MagicMock, patch
from src.memory.insight_layer_memory import InsightLayerMemory

@pytest.fixture
def memory():
    # Create an instance of InsightLayerMemory with a temporary directory
    with patch("src.memory.insight_layer_memory.os.makedirs"):
        memory = InsightLayerMemory()
        memory.insight_dir = "test_insights"  # Use a test directory
        os.makedirs(memory.insight_dir, exist_ok=True)
    yield memory
    # Cleanup after the test
    for fname in os.listdir(memory.insight_dir):
        os.remove(os.path.join(memory.insight_dir, fname))
    os.rmdir(memory.insight_dir)

@patch("src.memory.insight_layer_memory.VectorStore")
@patch("src.memory.insight_layer_memory.SentenceTransformer")
def test_increment_usage(mock_embedder, mock_vector_store, memory):
    # Mock the vector store and embedder
    mock_vector_store.return_value = MagicMock()
    mock_embedder.return_value = MagicMock()

    # Create a test insight
    insight = {
        "id": "test_insight",
        "what": "Test insight",
        "usage_count": 0,
        "links": [],
        "impact": 5,
        "outcome": 3,
        "recency": 2
    }
    memory.save_context(insight)

    # Increment usage
    memory.increment_usage("test_insight")

    # Verify the updated insight
    filename = os.path.join(memory.insight_dir, "test_insight.json")
    with open(filename, "r") as f:
        updated_insight = json.load(f)

    assert updated_insight["usage_count"] == 1
    assert "importance_score" in updated_insight
    assert updated_insight["importance_score"] > 0  # Ensure score is recalculated