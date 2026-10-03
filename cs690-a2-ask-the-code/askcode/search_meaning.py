"""Step 7: find chunks by meaning instead of by shared words.

YOUR CODE. Read HANDOUT.md, Step 7, first.
Check your work with:  pytest tests/test_search_meaning.py

The embedding model runs on your own laptop (askcode/embed.py). It is free and needs
no key; the first run downloads it once, about 67 MB, into the .models folder.
"""

from __future__ import annotations

import math
from collections.abc import Callable

from askcode import embed
from askcode.core import Chunk


def cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity of two vectors: dot(a, b) / (length(a) * length(b)).

    Return 0.0 if either vector has length 0 (all zeros).
    Raise ValueError if the two vectors do not have the same number of numbers.
    """
    if len(a) != len(b):
        raise ValueError(f"vectors have different sizes: {len(a)} and {len(b)}")
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    if length_a == 0 or length_b == 0:
        return 0.0
    return dot / (length_a * length_b)


class MeaningIndex:
    """Embed every chunk once, then answer many questions quickly (slides 43 to 46)."""

    def __init__(
        self,
        chunks: list[Chunk],
        embed_passages: Callable[[list[str]], list[list[float]]] | None = None,
        embed_query: Callable[[str], list[float]] | None = None,
    ) -> None:
        """Store the chunks and embed all of them, here, once, in a single call."""
        if embed_passages is None:
            embed_passages = embed.embed_passages
        if embed_query is None:
            embed_query = embed.embed_query
        self.chunks = list(chunks)
        self.embed_query = embed_query
        texts = [c.name + "\n" + c.text for c in self.chunks]
        self.vectors = [list(v) for v in embed_passages(texts)]

    def search(self, question: str, k: int = 3) -> list[Chunk]:
        """Return the k chunks whose vectors are closest in meaning to the question.

        The question is embedded once; every chunk is scored with cosine similarity;
        the highest scores come first, and ties keep the order of the chunks list.
        """
        q = self.embed_query(question)
        if k <= 0:
            return []
        scored = [(cosine(q, v), i) for i, v in enumerate(self.vectors)]
        scored.sort(key=lambda pair: (-pair[0], pair[1]))
        return [self.chunks[i] for _, i in scored[:k]]
