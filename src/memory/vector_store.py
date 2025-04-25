import os
import json
import faiss
import uuid
import numpy as np
from dotenv import load_dotenv
from typing import List, Dict
from langchain_community.embeddings import OpenAIEmbeddings
from src.models.insight_unit import InsightUnit
from src.utils.normalize_fields import normalize_insight
from .embedding_cache import EmbeddingCache

# Load environment variables
load_dotenv()

class VectorStore:
    def __init__(self, embedding_dim: int = 1536, index_path: str = "data/embeddings/index.faiss", metadata_path: str = "data/embeddings/metadata.json"):
        self.embedding_dim = embedding_dim
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.client = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.cache = EmbeddingCache()

        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        else:
            self.index = faiss.IndexFlatL2(embedding_dim)

        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, "r") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}

    def embed(self, text: str) -> List[float]:
        cached = self.cache.get(text)
        if cached:
            return cached
        embedding = self.client.embed_query(text)
        self.cache.set(text, embedding)
        return embedding

    def add_insight(self, insight_data: Dict) -> None:
        normalized = normalize_insight(insight_data)
        insight = InsightUnit(**normalized)
        text_parts = [
            insight.content.summary,
            insight.content.origin_method or "",
            insight.confidence.confidence_level if insight.confidence else "",
            insight.fidelity.fidelity_level if insight.fidelity else ""
        ]
        text = " ".join(text_parts)
        vector = self.embed(text)
        self.index.add(np.array([vector]).astype('float32'))

        idx_key = str(len(self.metadata))
        self.metadata[idx_key] = insight.id or f"insight_{uuid.uuid4().hex[:8]}"
        self._save()

    def search(self, query: str, top_k: int = 3) -> List[str]:
        vector = self.embed(query)
        D, I = self.index.search(np.array([vector]).astype('float32'), top_k)
        return [self.metadata[str(i)] for i in I[0] if str(i) in self.metadata]

    def _save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)
