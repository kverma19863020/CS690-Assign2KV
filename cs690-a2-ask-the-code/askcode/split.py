"""Step 2: split the codebase into chunks, one per function or method.

YOUR CODE. Read HANDOUT.md, Step 2, first.
Check your work with:  pytest tests/test_split.py
"""

from __future__ import annotations

import ast
from pathlib import Path

from askcode import CORPUS_DIR
from askcode.core import Chunk

_FUNCTION_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)


def _make_chunk(node: ast.AST, name: str, lines: list[str], file: str) -> Chunk:
    """Build one Chunk for a function node; the first decorator line starts it."""
    start = min([node.lineno] + [d.lineno for d in node.decorator_list])
    end = node.end_lineno
    text = "\n".join(lines[start - 1 : end])
    return Chunk(file=file, name=name, start_line=start, end_line=end, text=text)


def split_file(path: Path, root: Path) -> list[Chunk]:
    """Return one Chunk for every function and method in the Python file at `path`.

    Only top-level functions and methods of top-level classes become chunks.
    Methods are named "ClassName.method_name". A chunk starts at its first
    decorator. Lines are split on "\\n" so they match ast's line numbers.
    """
    source = Path(path).read_text(encoding="utf-8")
    lines = source.split("\n")
    file = Path(path).relative_to(root).as_posix()
    tree = ast.parse(source)

    chunks: list[Chunk] = []
    # Only tree.body (top level) and the bodies of top-level classes are visited,
    # so nested functions and functions inside if/try/for/while/with are skipped.
    for node in tree.body:
        if isinstance(node, _FUNCTION_TYPES):
            chunks.append(_make_chunk(node, node.name, lines, file))
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, _FUNCTION_TYPES):
                    chunks.append(_make_chunk(item, f"{node.name}.{item.name}", lines, file))
    return chunks


def split_corpus(root: Path = CORPUS_DIR) -> list[Chunk]:
    """Return the chunks of every .py file under `root`, sorted by relative path.

    For the requests codebase this returns 230 chunks.
    """
    root = Path(root)
    paths = sorted(root.rglob("*.py"), key=lambda p: p.relative_to(root).as_posix())
    chunks: list[Chunk] = []
    for path in paths:
        chunks.extend(split_file(path, root))
    return chunks
