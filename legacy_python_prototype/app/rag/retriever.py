import re
from typing import List, Dict
from app.rag.knowledge_base import KnowledgeBase
from app.utils.logger import get_logger

logger = get_logger(__name__)

def tokenize(text: str) -> set:
    text = text.lower()
    words = re.findall(r'\w+', text)
    # simple stopword removal
    stopwords = {"a", "an", "the", "and", "or", "to", "in", "of", "for", "is"}
    return set([w for w in words if w not in stopwords])

class Retriever:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.rules = self.kb.get_all_rules()
        self._build_index()

    def _build_index(self):
        if not self.rules:
            logger.warning("Knowledge base is empty. Retriever has no data to index.")
            return

        self.documents = []
        for rule in self.rules:
            text = f"{rule.get('item', '')} {rule.get('category', '')}"
            self.documents.append(tokenize(text))
        
        logger.info(f"Built keyword index with {len(self.rules)} documents.")

    def search(self, query: str, top_k: int = 2) -> List[Dict]:
        if not self.rules:
            return []
            
        query_tokens = tokenize(query)
        if not query_tokens:
            return []
            
        scores = []
        for idx, doc_tokens in enumerate(self.documents):
            # Calculate Jaccard-like similarity
            intersection = query_tokens.intersection(doc_tokens)
            score = len(intersection) / (len(query_tokens) + 0.1) # Avoid div by zero
            scores.append((score, self.rules[idx]))
            
        # Sort by score descending
        scores.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for score, rule in scores[:top_k]:
            if score > 0.0: # Must have at least one matching keyword
                results.append(rule)
                
        return results
