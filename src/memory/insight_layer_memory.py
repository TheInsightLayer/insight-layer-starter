# src/memory/insight_layer_memory.py

import os
import json
import yaml
import logging
from datetime import datetime
from typing import List, Dict, Optional
from functools import lru_cache
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer, util
from src.models.insight_unit import InsightUnit
from src.utils.normalize_fields import normalize_insight
from src.utils.scoring import compute_importance
from src.memory.vector_store import VectorStore

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InsightLayerMemory:
    def __init__(self, vault_path: str = "data/memory.db"):
        self.vault_path = vault_path
        self.insight_dir = os.path.join("data", "insights")
        os.makedirs(self.insight_dir, exist_ok=True)

        config_path = os.getenv("MEMORY_CONFIG_PATH", "configs/memory_config.yaml")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            self.similarity_threshold = config.get("similarity_threshold", 0.75)
        else:
            self.similarity_threshold = 0.75

        self.vector_store = VectorStore()
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    @lru_cache(maxsize=1000)
    def get_embedding(self, text: str):
        return self.embedder.encode(text, convert_to_tensor=True)

    def load_context(self, task_meta: Dict) -> List[Dict]:
        query = f"{task_meta['purpose']} {task_meta['topic']} {task_meta['quarter']}"
        insight_ids = self.vector_store.search(query)

        insights = []
        for insight_id in insight_ids:
            path = os.path.join(self.insight_dir, f"{insight_id}.json")
            if os.path.exists(path):
                with open(path, "r") as f:
                    insights.append(json.load(f))
        return insights

    def save_context(self, insight: Dict):
        normalized = normalize_insight(insight)
        validated = InsightUnit(**normalized)  # Validate against schema

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        validated.id = validated.id or f"insight_{timestamp}"
        fname = os.path.join(self.insight_dir, f"{validated.id}.json")

        # Auto-link related
        links = self._auto_link(validated)
        if links:
            validated.links = links

        # Write to disk
        with open(fname, "w") as f:
            json.dump(validated.dict(), f, indent=2)

        self.vector_store.add_insight(validated)
        print(f"[InsightLayerMemory] Saved: {validated.id}")

    def update_context(self, insight: Dict):
        normalized = normalize_insight(insight)
        validated = InsightUnit(**normalized)

        if not validated.id:
            raise ValueError("Insight must have an ID to update.")

        path = os.path.join(self.insight_dir, f"{validated.id}.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Insight {validated.id} not found.")

        with open(path, "w") as f:
            json.dump(validated.dict(), f, indent=2)

        self.vector_store.update_insight(validated)
        print(f"[InsightLayerMemory] Updated: {validated.id}")

    def delete_context(self, insight_id: str):
        path = os.path.join(self.insight_dir, f"{insight_id}.json")
        if os.path.exists(path):
            os.remove(path)
            self.vector_store.delete_insight(insight_id)
            print(f"[InsightLayerMemory] Deleted: {insight_id}")
        else:
            raise FileNotFoundError(f"Insight {insight_id} not found.")

    def increment_usage(self, insight_id: str):
        path = os.path.join(self.insight_dir, f"{insight_id}.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Insight {insight_id} not found.")

        with open(path, "r") as f:
            insight = json.load(f)

        insight["used_count"] = insight.get("used_count", 0) + 1
        weights = self._load_weights()
        insight["importance_score"] = compute_importance(insight, weights)

        with open(path, "w") as f:
            json.dump(insight, f, indent=2)

        print(f"[InsightLayerMemory] Incremented use and re-scored {insight_id}")

    def _auto_link(self, new_insight: InsightUnit) -> List[str]:
        """
        Compute similarity on 'what' field and return IDs of similar insights.
        """
        new_emb = self.get_embedding(new_insight.what)
        links = []

        for fname in os.listdir(self.insight_dir):
            if not fname.endswith(".json"):
                continue

            path = os.path.join(self.insight_dir, fname)
            with open(path, "r") as f:
                other = json.load(f)
                if other.get("id") == new_insight.id:
                    continue

                other_text = other.get("what", "")
                other_emb = self.get_embedding(other_text)
                similarity = util.pytorch_cos_sim(new_emb, other_emb).item()

                if similarity >= self.similarity_threshold:
                    links.append(other.get("id"))

        return links

    def _load_weights(self) -> Dict:
        path = os.getenv("IMPORTANCE_WEIGHTS_PATH", "configs/importance_weights.yaml")
        if os.path.exists(path):
            with open(path, "r") as f:
                return yaml.safe_load(f)
        else:
            return {"used": 0.4, "links": 0.3, "impact": 0.1, "outcome": 0.1, "recency": 0.1}
