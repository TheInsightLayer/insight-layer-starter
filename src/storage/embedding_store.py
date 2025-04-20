import os
import faiss
import pickle
import numpy as np
from langchain_openai import OpenAIEmbeddings

VECTOR_DB_PATH = "data/insight_faiss"
METADATA_PATH = "data/insight_metadata.pkl"

def embed_insights(insights):
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    texts = [item['insight'] for item in insights]
    meta = [item for item in insights]
    vectors = embeddings.embed_documents(texts)

    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(np.array(vectors).astype("float32"))

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(meta, f)
    faiss.write_index(index, VECTOR_DB_PATH)
    print(f"✅ Embedded {len(insights)} insights into FAISS.")

def search_insights(query, k=5):
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    index = faiss.read_index(VECTOR_DB_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    q_vec = embeddings.embed_query(query)
    D, I = index.search(np.array([q_vec]).astype("float32"), k)
    results = [metadata[i] for i in I[0] if i < len(metadata)]
    return results

def update_embedding(index, updated_item):
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    vector = embeddings.embed_query(updated_item['insight'])

    if not os.path.exists(VECTOR_DB_PATH):
        raise FileNotFoundError("Vector index not found. Run embed_insights() first.")

    index_file = faiss.read_index(VECTOR_DB_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    if index >= len(metadata):
        raise IndexError("Embedding index out of range")

    metadata[index] = updated_item
    index_file.remove_ids(faiss.IDSelector32(index))
    index_file.add_with_ids(np.array([vector]).astype("float32"), np.array([index]))

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)
    faiss.write_index(index_file, VECTOR_DB_PATH)
    print(f"🔁 Updated embedding for insight {index}")