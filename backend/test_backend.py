import os
import json
# pyrefly: ignore [missing-import]
import pytest
from backend.query_parser import parse_query
from backend.generator import generate_synthetic_corpus
from backend.indexer import build_index
from backend.search import SearchEngine
from backend.main import health, search, stats, startup_event

@pytest.fixture(scope="module", autouse=True)
def setup_data_and_index():
    generate_synthetic_corpus(total_messages=4200)
    build_index()
    startup_event()

def test_generator():
    base_dir = os.path.dirname(__file__)
    msgs_path = os.path.join(base_dir, "data", "messages.json")
    assert os.path.exists(msgs_path)
    with open(msgs_path, "r", encoding="utf-8") as f:
        msgs = json.load(f)
    assert len(msgs) >= 4000
    participants = set(m["sender"] for m in msgs)
    assert len(participants) == 8

def test_query_parser():
    res1 = parse_query("What did Priya say about the budget?")
    assert res1["intent"] == "person"
    assert res1["person"] == "Priya"
    
    res2 = parse_query("When did we decide on the trip?")
    assert res2["intent"] == "decision"
    
    res3 = parse_query("What happened last month?")
    assert res3["intent"] == "time"
    assert res3["time_range"] is not None

def test_search_engine_zero_overlap():
    engine = SearchEngine()
    res = engine.search("When did we decide on the trip?", mode="hybrid", top_k=5)
    assert len(res["results"]) > 0
    
    assert res["results"][0]["message_id"] == "msg_trip_decide"
    assert all(
        context_message["thread_id"] == "thread_trip"
        for context_message in res["results"][0]["context"]
    )

def test_api_endpoints():
    h_data = health()
    assert h_data["status"] == "ok"
    assert h_data["indexed_messages"] >= 4000
    
    s_data = search(q="When did we decide on the trip?", mode="hybrid")
    assert len(s_data["results"]) > 0
    
    st_data = stats()
    assert "corpus" in st_data
    assert "evaluation" in st_data
