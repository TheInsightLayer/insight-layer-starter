
import hashlib
import os
import json

class EmbeddingCache:
    def __init__(self, cache_path="data/embeddings/cache.json"):
        self.cache_path = cache_path
        self.cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r") as f:
                return json.load(f)
        return {}

    def get(self, text):
        key = hashlib.md5(text.encode()).hexdigest()
        return self.cache.get(key)

    def set(self, text, embedding):
        key = hashlib.md5(text.encode()).hexdigest()
        self.cache[key] = embedding
        self._save_cache()

    def _save_cache(self):
        with open(self.cache_path, "w") as f:
            json.dump(self.cache, f, indent=2)
