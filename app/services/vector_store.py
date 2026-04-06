from __future__ import annotations

from collections import Counter
from math import sqrt
from typing import Dict, List

from app.knowledge.base import DOCUMENTS


class InMemoryVectorStore:
    def __init__(self) -> None:
        self.documents = DOCUMENTS
        self.index = [self._tokenize(doc["text"] + " " + doc["topic"]) for doc in self.documents]

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        query_tokens = self._tokenize(query)
        scored = []
        for doc, doc_tokens in zip(self.documents, self.index):
            score = self._cosine_similarity(query_tokens, doc_tokens)
            if score > 0:
                scored.append({**doc, "score": round(score, 4)})
        ranked = sorted(scored, key=lambda item: item["score"], reverse=True)
        return ranked[:top_k]

    def _tokenize(self, text: str) -> Counter:
        tokens = [token.strip(".,:;!?()[]{}\n\t").lower() for token in text.split()]
        clean_tokens = [token for token in tokens if token]
        return Counter(clean_tokens)

    def _cosine_similarity(self, left: Counter, right: Counter) -> float:
        if not left or not right:
            return 0.0
        intersection = set(left.keys()) & set(right.keys())
        numerator = sum(left[token] * right[token] for token in intersection)
        left_norm = sqrt(sum(value * value for value in left.values()))
        right_norm = sqrt(sum(value * value for value in right.values()))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return numerator / (left_norm * right_norm)
