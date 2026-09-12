import json
import os
# pyrefly: ignore [missing-import]
import faiss
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

def build_index():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "data", "messages.json")
    index_dir = os.path.join(base_dir, "index")
    os.makedirs(index_dir, exist_ok=True)
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Messages corpus not found at {data_path}. Run generator.py first.")
        
    with open(data_path, "r", encoding="utf-8") as f:
        messages = json.load(f)
        
    print(f"Loading embedding model: {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)
    
    # Keep message vectors focused on the target text. Conversation context is
    # used by the reranker and result reconstruction, where it does not dilute
    # the semantic representation of a short decision message.
    texts = [message["text"] for message in messages]
    print(f"Generating embeddings for {len(texts)} messages...")
    embeddings = model.encode(texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True)
    embeddings = np.array(embeddings, dtype=np.float32)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    
    faiss_path = os.path.join(index_dir, "messages.faiss")
    faiss.write_index(index, faiss_path)
    
    id_map = {i: m["id"] for i, m in enumerate(messages)}
    id_map_path = os.path.join(index_dir, "id_map.json")
    with open(id_map_path, "w", encoding="utf-8") as f:
        json.dump(id_map, f, indent=2)

    threads = {}
    for message in messages:
        threads.setdefault(message["thread_id"], []).append(message)
    thread_ids = sorted(threads)
    thread_texts = [
        " ".join(message["text"] for message in threads[thread_id])
        for thread_id in thread_ids
    ]
    print(f"Generating embeddings for {len(thread_texts)} conversation threads...")
    thread_embeddings = model.encode(
        thread_texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,
    )
    thread_embeddings = np.array(thread_embeddings, dtype=np.float32)
    thread_index = faiss.IndexFlatIP(thread_embeddings.shape[1])
    thread_index.add(thread_embeddings)
    faiss.write_index(thread_index, os.path.join(index_dir, "threads.faiss"))
    with open(os.path.join(index_dir, "thread_map.json"), "w", encoding="utf-8") as f:
        json.dump({index: thread_id for index, thread_id in enumerate(thread_ids)}, f, indent=2)
        
    print(f"Index successfully built and saved to {faiss_path}")

if __name__ == "__main__":
    build_index()
