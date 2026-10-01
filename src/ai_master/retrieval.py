from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass


TOKEN = re.compile(r"[\wÀ-ỹ]+", re.UNICODE)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN.findall(text)]


@dataclass
class TfidfRetriever:
    documents: list[str]

    def __post_init__(self) -> None:
        self.term_counts = [Counter(tokenize(doc)) for doc in self.documents]
        self.document_frequency = Counter(term for counts in self.term_counts for term in counts)

    def _vector(self, counts: Counter[str]) -> dict[str, float]:
        total = sum(counts.values()) or 1
        return {term: (count / total) * math.log((1 + len(self.documents)) / (1 + self.document_frequency[term])) for term, count in counts.items()}

    def search(self, query: str, k: int = 3) -> list[tuple[int, float]]:
        if k < 1:
            raise ValueError("k must be positive")
        query_vector = self._vector(Counter(tokenize(query)))
        query_norm = math.sqrt(sum(value * value for value in query_vector.values())) or 1.0
        scored = []
        for index, counts in enumerate(self.term_counts):
            vector = self._vector(counts)
            norm = math.sqrt(sum(value * value for value in vector.values())) or 1.0
            score = sum(query_vector.get(term, 0.0) * value for term, value in vector.items()) / (query_norm * norm)
            scored.append((index, score))
        return sorted(scored, key=lambda item: (-item[1], item[0]))[:k]

