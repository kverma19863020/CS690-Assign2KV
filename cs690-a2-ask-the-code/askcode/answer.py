"""Step 4, part B: check the AI's reply before your program trusts it.

YOUR CODE. Read HANDOUT.md, Step 4, first.
Check your work with:  pytest tests/test_answer.py
"""

from __future__ import annotations

import json

from askcode.core import BadReply

KEYS = {"answer", "file", "line"}


def _no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    """json.loads hook: a key that appears twice makes the reply ambiguous, so reject it."""
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise BadReply(f"key {key!r} appears more than once")
        result[key] = value
    return result


def _strip_fence(text: str) -> str:
    """Remove one Markdown code fence around the reply, if there is one (rule 1)."""
    lines = text.split("\n")
    first = lines[0].strip()
    if first.startswith("```"):
        if first not in ("```", "```json"):
            raise BadReply("the opening code fence must be ``` or ```json")
        if len(lines) < 3 or lines[-1].strip() != "```":
            raise BadReply("an opening code fence needs a closing ``` on the last line")
        return "\n".join(lines[1:-1]).strip()
    return text


def parse_reply(text: str) -> dict:
    """Check the model's reply and return {"answer": ..., "file": ..., "line": ...}.

    Raises BadReply, and only BadReply, when any of these fails:
    1. the reply (optionally inside one ``` or ```json fence) is exactly one JSON
       object, with no other text before or after it;
    2. the keys are exactly answer, file and line;
    3. answer is a string that is not empty or only whitespace;
    4. file is a non-empty string or null; line is an integer >= 1 (not a bool) or null;
    5. file and line are both null or both set.
    """
    try:
        if not isinstance(text, str):
            raise BadReply("the reply is not text")
        body = _strip_fence(text.strip())
        if not body:
            raise BadReply("the reply is empty")

        # Rule 1: json.loads fails on any extra text before or after the object.
        try:
            data = json.loads(body, object_pairs_hook=_no_duplicate_keys)
        except json.JSONDecodeError as exc:
            raise BadReply(f"the reply is not one JSON object: {exc.msg}") from None
        if not isinstance(data, dict):
            raise BadReply("the reply is JSON but not an object")

        # Rule 2: exactly the three keys.
        missing, extra = KEYS - data.keys(), data.keys() - KEYS
        if missing or extra:
            raise BadReply(f"wrong keys: missing {sorted(missing)}, extra {sorted(extra)}")

        answer, file, line = data["answer"], data["file"], data["line"]

        # Rule 3: answer is a non-blank string.
        if not isinstance(answer, str) or not answer.strip():
            raise BadReply("answer must be a non-empty string")

        # Rule 4: file is a non-empty string or null; line is an int >= 1 or null.
        if file is not None and (not isinstance(file, str) or file == ""):
            raise BadReply("file must be a non-empty string or null")
        if line is not None:
            if type(line) is not int:  # excludes True/False, floats and strings
                raise BadReply("line must be an integer or null")
            if line < 1:
                raise BadReply("line must be at least 1")

        # Rule 5: both null or both set.
        if (file is None) != (line is None):
            raise BadReply("file and line must both be null or both be set")

        return {"answer": answer, "file": file, "line": line}
    except BadReply:
        raise
    except Exception as exc:  # never let another exception escape
        raise BadReply(f"could not check the reply: {exc}") from None
