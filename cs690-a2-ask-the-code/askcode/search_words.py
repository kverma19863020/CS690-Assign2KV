"""Step 3: find the chunks that share the most useful words with the question.

YOUR CODE. Read HANDOUT.md, Step 3, first.
Check your work with:  pytest tests/test_search_words.py
"""

from __future__ import annotations

import math

from askcode.core import STOPWORDS, Chunk, words


def search_words(question: str, chunks: list[Chunk], k: int = 3) -> list[Chunk]:
    """Return up to k chunks that best match the question by shared words.

    Each question word w (stopwords removed) weighs log(N / df(w)), where N is the
    number of chunks and df(w) is how many chunks contain w. A chunk's score is the
    sum of the weights of the question words it contains, rounded to 6 places.
    Chunks scoring above 0 are returned, highest first; ties keep chunk order.
    """
    question_words = set(words(question)) - STOPWORDS
    if not question_words or not chunks:
        return []

    chunk_words = [set(words(c.name + "\n" + c.text)) for c in chunks]
    n = len(chunks)

    weights: dict[str, float] = {}
    for w in question_words:
        df = sum(1 for cw in chunk_words if w in cw)
        if df > 0:  # ignore question words no chunk contains
            weights[w] = math.log(n / df)

    scored = []
    for index, cw in enumerate(chunk_words):
        score = round(sum(weight for w, weight in weights.items() if w in cw), 6)
        if score > 0:
            scored.append((score, index))

    # Highest score first; on a tie, the smaller index (earlier chunk) comes first.
    scored.sort(key=lambda pair: (-pair[0], pair[1]))
    return [chunks[index] for _, index in scored[:k]]
