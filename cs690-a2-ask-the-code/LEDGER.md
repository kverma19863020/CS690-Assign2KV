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
