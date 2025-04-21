import os
import json
import logging
import yaml
from datetime import datetime
from typing import List, Dict
from functools import lru_cache
from .vector_store import VectorStore
from sentence_transformers import SentenceTransformer, util
import unittest
from unittest.mock import patch, MagicMock
from src.utils.scoring import compute_importance

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InsightLayerMemory:
    def __init__(self, vault_path: str = "data/memory.db"):
        self.vault_path = vault_path
        self.insight_dir = os.path.join("data", "insights")
        os.makedirs(self.insight_dir, exist_ok=True)

        # Load configuration
        config_path = os.path.join("configs", "memory_config.yaml")
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        self.similarity_threshold = config.get("similarity_threshold", 0.75)

        # Vector search + semantic comparison
        self.vector_store = VectorStore()
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    @lru_cache(maxsize=1000)
    def get_embedding(self, text: str):
        return self.embedder.encode(text, convert_to_tensor=True)

    def load_context(self, task_meta: Dict) -> List[Dict]:
        """
        Retrieve insights relevant to the task using vector-based semantic search.
        """
        query = f"{task_meta['purpose']} {task_meta['topic']} {task_meta['quarter']}"
        insight_ids = self.vector_store.search(query)

        insights = []
        for insight_id in insight_ids:
            fname = os.path.join(self.insight_dir, f"{insight_id}.json")
            if os.path.exists(fname):
                with open(fname, "r") as f:
                    insights.append(json.load(f))
        return insights

    def save_context(self, insight: Dict):
        """
        Save the new InsightUnit to disk, auto-link it, and update the vector index.
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        insight_id = f"insight_{timestamp}"
        insight["id"] = insight_id

        # Auto-link to related insights
        links = self._auto_link(insight)
        if links:
            insight["links"] = links

        filename = os.path.join(self.insight_dir, f"{insight_id}.json")
        with open(filename, "w") as f:
            json.dump(insight, f, indent=2)

        self.vector_store.add_insight(insight, insight_id)
        print(f"[Insight Layer Memory] Insight saved and indexed as {insight_id}")

    def update_context(self, insight: Dict):
        """
        Update an existing InsightUnit on disk and in the vector index.
        """
        insight_id = insight.get("id")
        if not insight_id:
            raise ValueError("Insight must have an 'id' to be updated.")

        filename = os.path.join(self.insight_dir, f"{insight_id}.json")
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Insight with ID {insight_id} does not exist.")

        with open(filename, "w") as f:
            json.dump(insight, f, indent=2)

        self.vector_store.update_insight(insight, insight_id)
        print(f"[Insight Layer Memory] Insight {insight_id} updated.")

    def delete_context(self, insight_id: str):
        """
        Delete an InsightUnit from disk and the vector index.
        """
        filename = os.path.join(self.insight_dir, f"{insight_id}.json")
        if os.path.exists(filename):
            os.remove(filename)
            self.vector_store.delete_insight(insight_id)
            print(f"[Insight Layer Memory] Insight {insight_id} deleted.")
        else:
            raise FileNotFoundError(f"Insight with ID {insight_id} does not exist.")

    def increment_usage(self, insight_id: str):
        """
        Increment the usage count of an insight and recalculate its importance score.
        """
        filename = os.path.join(self.insight_dir, f"{insight_id}.json")
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Insight with ID {insight_id} does not exist.")

        with open(filename, "r") as f:
            insight = json.load(f)

        # Increment usage count
        insight["used_count"] = insight.get("used_count", 0) + 1

        # Recalculate importance score
        weights = self._load_weights()
        insight["importance_score"] = compute_importance(insight, weights)

        # Save updated insight
        with open(filename, "w") as f:
            json.dump(insight, f, indent=2)

        print(f"[InsightLayerMemory] Usage incremented and score recalculated for {insight_id}")

    def _load_weights(self):
        """
        Load scoring weights from the configuration file.
        """
        config_path = os.path.join("configs", "importance_weights.yaml")
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    def _compute_importance(self, insight: Dict, weights: Dict) -> float:
        """
        Compute the importance score for an insight based on weights.
        """
        return (
            weights.get("used", 0.4) * insight.get("usage_count", 0) +
            weights.get("links", 0.3) * len(insight.get("links", [])) +
            weights.get("impact", 0.1) * insight.get("impact", 0) +
            weights.get("outcome", 0.1) * insight.get("outcome", 0) +
            weights.get("recency", 0.1) * insight.get("recency", 0)
        )

    def _auto_link(self, new_insight: Dict) -> List[str]:
        """
        Find related insights using semantic similarity on the 'what' field.
        Returns a list of related insight IDs.
        """
        new_embedding = self.get_embedding(new_insight.get("what", ""))
        links = []

        for fname in os.listdir(self.insight_dir):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(self.insight_dir, fname)
            with open(fpath, "r") as f:
                existing = json.load(f)
                existing_id = existing.get("id") or fname.replace(".json", "")
                if existing_id == new_insight.get("id"):
                    continue

                existing_text = existing.get("what", "")
                existing_embedding = self.get_embedding(existing_text)

                similarity = util.pytorch_cos_sim(new_embedding, existing_embedding).item()
                if similarity >= self.similarity_threshold:
                    links.append(existing_id)

        return links

class TestInsightLayerMemory(unittest.TestCase):
    def setUp(self):
        self.memory = InsightLayerMemory()
        self.memory.insight_dir = "test_insights"
        os.makedirs(self.memory.insight_dir, exist_ok=True)

    def tearDown(self):
        for fname in os.listdir(self.memory.insight_dir):
            os.remove(os.path.join(self.memory.insight_dir, fname))
        os.rmdir(self.memory.insight_dir)

    @patch("sentence_transformers.SentenceTransformer.encode")
    def test_auto_link(self, mock_encode):
        mock_encode.side_effect = lambda text, convert_to_tensor: [1.0] if "new" in text else [0.5]
        new_insight = {"id": "new_insight", "what": "new insight text"}
        existing_insight = {"id": "existing_insight", "what": "existing insight text"}
        with open(os.path.join(self.memory.insight_dir, "existing_insight.json"), "w") as f:
            json.dump(existing_insight, f)

        links = self.memory._auto_link(new_insight)
        self.assertEqual(links, ["existing_insight"])
