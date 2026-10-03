# Provenance Ledger

Write one entry per reviewable change or experiment, when the work is done. Use exactly
the schema in HANDOUT.md. Put the prompts you typed into AI tools in `prompts/` and name
the file in the entry's `prompts` field.

## Worked example (not graded; leave it here and add your entries under "My entries")

This shows the level of detail expected. The commit SHAs, dates and numbers are made up.

```
## Entry 2
artifact:  askcode/split.py at commit 3f2a9c1
tool:      GitHub Copilot Chat in VS Code, model Claude Haiku 4.5, 2026-09-22
prompts:   asked for an ast loop that returns methods with class-qualified names;
           prompts/split-01.md
review:    read every line; rejected its use of ast.walk, which also returned nested
           functions and broke rule 1; rewrote the loop over tree.body and class bodies
           myself; kept its decorator handling after checking it against rule 3
checks:    pytest tests/test_split.py: 8 passed
evidence:  HANDOUT Step 2, split.py docstring rules 1 to 6
risk:      I did not test a file with Windows line endings

## Entry 5
artifact:  results/top3_words_five_part.csv at commit 8d41e07
tool:      askcode run_eval, anthropic claude-haiku-4-5-20251001, 2026-09-23
prompts:   the five-part prompt in askcode/prompt.py at commit 8d41e07;
           prompts/five-part-v1.md
review:    read all ten replies and marked the correct column against questions.json
checks:    python -m askcode.run_eval --search words --context top3 --prompt five_part:
           valid JSON 10 of 10, right place 6 of 10
evidence:  HANDOUT Step 5
risk:      one run only; a fresh run may answer differently
dataset:   questions/questions.json at commit 51c0e2a; corpus requests v2.32.3
result:    correct 6 of 10, 24,113 input tokens; results/top3_words_five_part.csv
changed:   two misses were retrieval failures, so I looked at why word search missed
           them before touching the prompt
```

## My entries

## Entry 1
artifact:  environment setup and .env configuration (.env not committed)
tool:      Claude (claude.ai), Claude Opus 5.5, 2026-10-03, for setup guidance;
           API provider OpenAI, model gpt-5.6-luna
prompts:   asked how to set up the repo and where to find my model's prices;
           prompts/entry-01-setup.md
review:    read the prices myself on https://platform.openai.com/docs/pricing:
           gpt-5.6-luna short context, input $0.20 / MTok, output $1.20 / MTok;
           chose short context because no prompt here reaches the long-context size;
           kept the default model instead of the cheaper gpt-6-luna, as the handout says
checks:    python -m askcode.check_setup: All checks passed (AI call 13 tokens in, 4 out);
           git status: .env not listed
evidence:  HANDOUT Step 0
risk:      prices may change before my runs; result costs are estimates from these prices

## Entry 2
artifact:  questions/questions.json at the "Freeze my questions" commit
tool:      Claude (claude.ai), Claude Opus 5.5, 2026-10-03
prompts:   asked Claude to draft my ten questions; prompts/entry-02-questions.md
review:    Claude drafted all ten questions and answers; I read every expected
           function with ~/show.py and checked each answer and line range against
           the code before freezing
checks:    load_questions: 10 questions, 1 unanswerable; show.py found all 9 named
           functions; pytest tests/test_questions.py not run yet (needs Step 2 splitter)
evidence:  HANDOUT Step 1; tests/test_questions.py
risk:      questions were AI-drafted rather than written in class; answer wording
           may need judgment when marking replies as right or wrong

## Entry 3
artifact:  askcode/split.py at the "Step 2: split.py, 230 chunks" commit
tool:      Claude (claude.ai), Claude Opus 5.5, 2026-10-03
prompts:   asked Claude for step-by-step help; it drafted split.py; prompts/entry-03-split.md
review:    read every line against docstring rules 1 to 6; confirmed it loops over
           tree.body and top-level class bodies only (not ast.walk), so nested functions
           and functions inside if/try are skipped; confirmed decorators start the chunk
           and lines are split on "\n"
checks:    pytest tests/test_split.py tests/test_questions.py: 12 passed
evidence:  HANDOUT Step 2; split.py docstring rules 1 to 6
risk:      not tested on files with Windows line endings or syntax errors

## Entry 4
artifact:  askcode/search_words.py and results/retrieval_words.csv at the
           "Step 3: search_words.py and retrieval_words results" commit
tool:      Claude (claude.ai), Claude Opus 5.5, 2026-10-03; askcode run_eval (no AI calls)
prompts:   Claude drafted search_words.py; prompts/entry-04-search-words.md
review:    read every line against docstring scoring rules 1 to 6; checked that
           question and chunk words are sets, weight is log(N/df), words with df 0
           are ignored, scores are rounded to 6 places before sorting, and ties keep
           chunk order; confirmed the handout weights (authorization 3.36, self 0.39)
checks:    pytest tests/test_search_words.py: 7 passed;
           python -m askcode.run_eval --search words --no-ai: right function in top 3
           for 5 of 9 answerable questions; python -m askcode.check_freeze: passed
evidence:  HANDOUT Step 3; search_words.py docstring rules 1 to 6
risk:      plain word overlap, no BM25 term-frequency or length adjustment; questions
           phrased without code words may be missed

## Entry 5
artifact:  askcode/prompt.py and askcode/answer.py at the
           "Step 4: five-part prompt and reply checker" commit
tool:      Claude (claude.ai), Claude Opus 5.5, 2026-10-03
prompts:   Claude drafted both files; prompts/entry-05-prompt-answer.md
review:    prompt.py: checked the five labels are in order, system text never includes
           the question or code (so it is identical on every call), rules include the
           "not found in the code shown" reply with null file and line, and the example
           (Session.close) is not one of my questions. answer.py: checked the fence
           rule, exact keys, type(line) is int so true/false are rejected, file and line
           both null or both set, and that every failure is raised as BadReply
checks:    pytest tests/test_prompt.py tests/test_answer.py: 22 passed;
           python -m askcode.run_eval --search words --context top3 --prompt five_part
           --dry-run: about 25,978 input tokens, about $0.0052 estimated input cost
evidence:  HANDOUT Step 4; prompt.py requirements 1 to 6; answer.py rules 1 to 5
risk:      a reply can pass the check and still be wrong; that is measured in Step 5

## Entry 6
artifact:  results/top3_words_five_part.csv, whole_five_part.csv, gold_five_part.csv
           and ai_replies/ at the "Step 5: mark top3 not-found replies as wrong" commit
tool:      askcode run_eval, openai gpt-5.6-luna, 2026-10-03; Claude (claude.ai),
           Claude Opus 5.5, for marking help and fault labels
prompts:   the five-part prompt in askcode/prompt.py at commit e4c274a;
           prompts/entry-06-step5-runs.md
review:    read every reply against questions.json; first marked all 30 yes, then found
           that q02, q05, q06, q07 and q08 in top3 replied "not found in the code shown"
           for answerable questions and corrected them to no; kept q10 yes in all runs
checks:    python -m askcode.run_eval --search words --context top3 --prompt five_part,
           --context whole, --context gold: valid JSON 10 of 10 in all three;
           python -m askcode.summary: Table 3 lists 5 wrong top3 answers
evidence:  HANDOUT Step 5; REPORT section 1
risk:      one run per setting; a fresh run may answer differently; marks are my
           judgment against one-sentence expected answers
dataset:   questions/questions.json at commit 177461d; corpus requests v2.32.3
result:    correct top3 5 of 10 (24,295 input tokens, $0.0054), whole 10 of 10
           (549,348 input tokens, $0.1104), gold 10 of 10 (7,649 input tokens,
           $0.0021); faults: 4 retrieval (q02, q05, q06, q08), 1 generation (q07)
changed:   since 4 of 5 misses were retrieval failures, I will fix retrieval
           (meaning search, Step 7) before changing the prompt; I also learned to
           mark "not found" as no when the question has a real answer

## Entry 7
artifact:  results/top3_words_minimal.csv and ai_replies/ at the
           "Step 6: minimal prompt run, marked" commit; REPORT sections 2 and 3
tool:      askcode run_eval, openai gpt-5.6-luna, 2026-10-03; Claude (claude.ai),
           Claude Opus 5.5, for comparing replies and drafting the report text
prompts:   the fixed build_prompt_minimal in askcode/core.py;
           prompts/entry-07-step6-minimal.md
review:    marked all 7 invalid-JSON rows no; read the 3 valid replies (q03, q07, q10)
           and marked them yes; compared q01 raw replies from both prompts and found the
           minimal reply put "line": "997–1024" (a string), which parse_reply rejects
checks:    python -m askcode.run_eval --search words --context top3 --prompt minimal:
           valid JSON 3 of 10, right place 1 of 10; python -m askcode.summary: Table 2
evidence:  HANDOUT Step 6; REPORT section 3
risk:      one run only; q07's yes depends on accepting an invented example version
dataset:   questions/questions.json at commit 177461d; same top 3 word-search
           results as top3_words_five_part
result:    minimal: correct 3 of 10, right place 1 of 10, valid JSON 3 of 10,
           20,235 in / 2,548 out tokens, $0.0071; five-part: correct 5 of 10, right
           place 5 of 10, valid JSON 10 of 10, 24,295 in / 457 out tokens, $0.0054
changed:   kept the five-part prompt for all remaining runs; the reply-format rules and
           example are what made the JSON usable, and they also cut output tokens
           by more than 5 times

## Entry 8
artifact:  askcode/search_meaning.py and results/retrieval_meaning.csv at the
           "Step 7: meaning search and retrieval_meaning results" commit
tool:      Claude (claude.ai), Claude Opus 5.5, 2026-10-03; local embedding model
           BAAI/bge-small-en-v1.5 via askcode/embed.py
prompts:   Claude drafted search_meaning.py and report sections 4 and 5;
           prompts/entry-08-meaning.md
review:    checked cosine returns 0.0 for a zero vector and raises ValueError for
           different sizes; checked __init__ calls embed_passages exactly once on
           name + "\n" + text, and search embeds only the question, sorts by score
           with ties in chunk order, and always returns k chunks
checks:    pytest tests/test_search_meaning.py: 6 passed;
           python -m askcode.run_eval --search meaning --no-ai: right function in
           top 3 for 7 of 9 answerable questions
evidence:  HANDOUT Step 7; search_meaning.py docstrings; REPORT section 4
risk:      I did not run the AI on meaning-search results, so its answer accuracy
           is not measured, only its retrieval
dataset:   questions/questions.json at commit 177461d; corpus requests v2.32.3
result:    retrieval_meaning 7 of 9 against retrieval_words 5 of 9; meaning ranked
           q01, q02, q03, q08 and q09 higher; word search ranked none higher;
           both missed q05 and q06 (Table 4)
changed:   my decision rule in REPORT section 5 prefers meaning search over word
           search for everyday questions
