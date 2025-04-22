import os
import faiss
import json
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
from typing import List, Dict
from dotenv import load_dotenv
from .embedding_cache import EmbeddingCache

# Load environment variables
load_dotenv()

class VectorStore:
    def __init__(self, embedding_dim: int = 1536, index_path: str = "data/embeddings/index.faiss", metadata_path: str = "data/embeddings/metadata.json"):
        self.embedding_dim: int = embedding_dim
        self.index_path: str = index_path
        self.metadata_path: str = metadata_path
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

    def add_insight(self, insight: Dict[str, str], insight_id: str) -> None:
        text = f"{insight['what']} {insight['why']} {insight['how']} {insight['outcome']}"
        vector = self.embed(text)
        self.index.add(np.array([vector]).astype('float32'))
        self.metadata[str(len(self.metadata))] = insight_id
        self._save()

    def search(self, query: str, top_k: int = 3) -> List[str]:
        vector = self.embed(query)
        D, I = self.index.search(np.array([vector]).astype('float32'), top_k)
        return [self.metadata[str(i)] for i in I[0] if str(i) in self.metadata]

    def _save(self) -> None:
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)
