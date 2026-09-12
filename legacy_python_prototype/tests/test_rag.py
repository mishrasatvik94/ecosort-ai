import pytest
import os
import json
from app.rag.knowledge_base import KnowledgeBase
from app.rag.retriever import Retriever

@pytest.fixture
def mock_kb(tmp_path):
    cat_file = tmp_path / "categories.json"
    rules_file = tmp_path / "rules.json"
    
    cat_file.write_text(json.dumps([{"name": "Organic"}, {"name": "E-Waste"}]))
    rules_file.write_text(json.dumps([
        {"item": "banana peel", "category": "Organic", "handling": "Compost"},
        {"item": "battery", "category": "E-Waste", "handling": "Recycle center"}
    ]))
    
    return KnowledgeBase(str(cat_file), str(rules_file))

def test_retriever_search_banana(mock_kb):
    retriever = Retriever(mock_kb)
    results = retriever.search("banana peel Organic")
    
    assert len(results) >= 1
    assert results[0]["item"] == "banana peel"

def test_retriever_empty_search(mock_kb):
    retriever = Retriever(mock_kb)
    results = retriever.search("asdfasdf")
    
    # Depending on TF-IDF it might return empty or low similarity
    # We filter by similarity > 0.1, so it should be empty
    assert len(results) == 0
