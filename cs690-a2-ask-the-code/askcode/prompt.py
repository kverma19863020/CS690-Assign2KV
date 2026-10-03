"""Step 4, part A: the five-part prompt from the Week 3 slides.

YOUR CODE. Read HANDOUT.md, Step 4, first.
Check your work with:  pytest tests/test_prompt.py
"""

from __future__ import annotations

from askcode.core import NO_CODE, Chunk, Prompt, format_chunk

# The stable part of the prompt. It never mentions the question or the code, so it
# is byte-for-byte the same on every call and can go first (and be cached).
SYSTEM = """Goal:
You answer questions about the Python source code of the requests library. A
developer who is new to the code asks one question; you give a short, accurate answer
and point to the file and line in the code shown that supports it.

Inputs and outputs:
Input: a "Code:" section with one or more pieces of code, then a "Question:" line.
Each piece starts with a header "### <file>, <function>, lines <start> to <end>",
and every code line after it starts with its line number and a colon.
Output: one JSON object with your answer, the file, and the line number.

Rules:
1. Answer only from the code shown. Do not use what you know about requests from
   anywhere else, and do not guess.
2. If the code shown does not answer the question, reply with the answer
   "not found in the code shown" and null for both file and line.
3. "file" is the file name exactly as written in the header of the piece you used,
   for example "sessions.py".
4. "line" is one line number, taken from the numbers shown at the start of the code
   lines, of the line that best supports your answer.
5. Keep the answer to one or two sentences and name the specific values, codes or
   conditions the code uses.

Example:
Question: What does closing a session do to its adapters?
Reply:
{"answer": "Session.close loops over every adapter mounted on the session and calls close() on each one.", "file": "sessions.py", "line": 796}

Reply format:
Reply with exactly one JSON object and nothing before or after it: no explanation,
no greeting, no Markdown. The object has exactly these three keys:
"answer": a string,
"file": a string, or null when the answer is not found in the code shown,
"line": an integer, or null when the answer is not found in the code shown."""


def build_prompt_five_part(question: str, chunks: list[Chunk]) -> Prompt:
    """Build the prompt your pipeline sends to the AI.

    system is the fixed five-part text above (Goal, Inputs and outputs, Rules,
    Example, Reply format). user is "Code:", the chunks (or NO_CODE), then
    "Question:" and the question, last.
    """
    code = "\n\n".join(format_chunk(c) for c in chunks) if chunks else NO_CODE
    user = f"Code:\n{code}\n\nQuestion:\n{question}"
    return Prompt(system=SYSTEM, user=user)
