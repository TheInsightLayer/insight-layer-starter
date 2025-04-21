
import os
import faiss
import json
import numpy as np
from openai import OpenAI
from typing import List, Dict
from .embedding_cache import EmbeddingCache

class VectorStore:
    def __init__(self, embedding_dim=1536, index_path="data/embeddings/index.faiss", metadata_path="data/embeddings/metadata.json"):
        self.embedding_dim = embedding_dim
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.client = OpenAI()
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

        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=[text]
        )
        embedding = response.data[0].embedding
        self.cache.set(text, embedding)
        return embedding

    def add_insight(self, insight: Dict, insight_id: str):
        text = f"{insight['what']} {insight['why']} {insight['how']} {insight['outcome']}"
        vector = self.embed(text)
        self.index.add(np.array([vector]).astype('float32'))
        self.metadata[str(len(self.metadata))] = insight_id
        self._save()

    def search(self, query: str, top_k=3) -> List[str]:
        vector = self.embed(query)
        D, I = self.index.search(np.array([vector]).astype('float32'), top_k)
        return [self.metadata[str(i)] for i in I[0] if str(i) in self.metadata]

    def _save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)
