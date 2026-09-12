import json
import os
from contextlib import asynccontextmanager
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Query, HTTPException
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from backend.search import SearchEngine
from backend.evaluate import run_evaluation

search_engine = None

def startup_event():
    global search_engine
    try:
        search_engine = SearchEngine()
        print("Search Engine initialized successfully.")
    except Exception as e:
        print(f"Warning: SearchEngine startup error: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup_event()
    yield


app = FastAPI(
    title="ContextFind API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    indexed_count = len(search_engine.messages) if search_engine else 0
    return {
        "status": "ok",
        "indexed_messages": indexed_count,
        "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2"
    }

@app.get("/search")
def search(q: str = Query(..., min_length=1), mode: str = Query("hybrid")):
    if not search_engine:
        raise HTTPException(status_code=503, detail="Search engine not initialized.")
    if mode not in ["hybrid", "semantic", "keyword"]:
        raise HTTPException(status_code=400, detail="Invalid mode. Choose hybrid, semantic, or keyword.")
        
    res = search_engine.search(query=q, mode=mode, top_k=10)
    return res

@app.get("/stats")
def stats():
    base_dir = os.path.dirname(__file__)
    eval_path = os.path.join(base_dir, "data", "eval_results.json")
    
    if os.path.exists(eval_path):
        with open(eval_path, "r", encoding="utf-8") as f:
            eval_data = json.load(f)
    else:
        eval_data = run_evaluation()
        
    msg_count = len(search_engine.messages) if search_engine else 4200
    
    return {
        "corpus": {
            "total_messages": msg_count,
            "participants": 8,
            "timespan_months": 6
        },
        "evaluation": eval_data
    }

if __name__ == "__main__":
    # pyrefly: ignore [missing-import]
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
