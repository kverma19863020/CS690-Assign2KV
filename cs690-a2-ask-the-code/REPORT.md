# Assignment 2 Report: Ask the Code

Name: Ketan Verma
Provider and model: OpenAI, gpt-5.6-luna
Prices used (per million tokens, input and output), and the page you found them on: $0.20 input and $1.20 output per million tokens (short context), https://platform.openai.com/docs/pricing

## Table 1. Finding the right function

| Run | Right function in top 3 |
| --- | --- |
| retrieval_words | 5 of 9 |
| retrieval_meaning | 7 of 9 |

## Table 2. Answers

| Run | Valid JSON | Right place | Correct (your marks) | Input tokens | Output tokens | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- |
| top3_words_five_part | 10 of 10 | 5 of 10 | 5 of 10 | 24,295 | 457 | 0.0054 |
| whole_five_part | 10 of 10 | 10 of 10 | 10 of 10 | 549,348 | 464 | 0.1104 |
| gold_five_part | 10 of 10 | 10 of 10 | 10 of 10 | 7,649 | 443 | 0.0021 |
| top3_words_minimal | 3 of 10 | 1 of 10 | 3 of 10 | 20,235 | 2,548 | 0.0071 |

## 1. Whose fault is it? (Step 5)

One row for every question marked `no` in top3_words_five_part. Take the first three
columns from Table 3 of `python -m askcode.summary`. Fault is retrieval, generation or
both, following the rule in Step 5. Evidence is one sentence about what you saw in the
reply or the retrieved functions.

| Question | Hit in top 3 | Correct with gold context | Fault | Evidence |
| --- | --- | --- | --- | --- |
| q02 | no | yes | retrieval | Word search returned HTTPAdapter.send, SessionRedirectMixin.resolve_redirects and api.request instead of prepare_content_length, so the AI said not found; given the gold function it answered correctly. |
| q05 | no | yes | retrieval | The top 3 were HTTPAdapter.send, should_strip_auth and super_len, not merge_setting, so the AI never saw the code that deletes None-valued keys and said not found. |
| q06 | no | yes | retrieval | This plain-English question shares few words with get_encoding_from_headers, so word search returned Response.json, Response.__init__ and a connection-pool helper and the AI said not found. |
| q07 | yes | yes | generation | default_user_agent was ranked first, yet the AI replied not found, likely because the code shows f"{name}/{__version__}" without the version value, even though the expected answer only needs that format. |
| q08 | no | yes | retrieval | Word search ranked two connection-pool helpers and Session.request above HTTPDigestAuth.build_digest_header, so the AI never saw the algorithm list and said not found. |

## 2. Paste everything or search? (Step 5)

Compare top3_words_five_part with whole_five_part: correct answers, input tokens and cost
for each, from Table 2. In two or three sentences: did pasting the whole codebase give
better answers, and was the difference worth the price?

Pasting the whole codebase gave 10 of 10 correct answers against 5 of 10 for the
top 3 word-search functions, but it used 549,348 input tokens ($0.1104) against 24,295
($0.0054), about 23 times the tokens and 20 times the cost. At this codebase's size the
whole-codebase answers were better and the extra 10.5 cents for ten questions was small
in absolute terms, but the gold run (10 of 10 for 7,649 tokens, $0.0021) shows the gap
came from retrieval, so a better search could match the accuracy at a fraction of the price.

## 3. Minimal prompt against five-part prompt (Step 6)

Which prompt did better on right place, and which on correct? Give both numbers for both
prompts. Name one question where the two prompts' replies differed, and say what
differed.

The five-part prompt did better on both measures: right place 5 of 10 against 1 of 10
for the minimal prompt, and correct 5 of 10 against 3 of 10 (valid JSON 10 of 10 against
3 of 10). On q01 both replies stated the right facts (400 to 499 Client Error, 500 to 599
Server Error), but the minimal reply sent "line": "997–1024", a string range instead of
an integer, so parse_reply rejected it and it counts as wrong, while the five-part reply
gave the integer line 1013. The prompts also differed on q07: the five-part prompt said
not found, but the minimal prompt answered "python-requests/<version>" and filled in a
version (2.32.5) that is not in the code shown, since it had no rule to answer only from
the code.

## 4. Word search against meaning search (Step 7)

Name one question meaning search ranked higher than word search, and one question word
search ranked higher than meaning search, with the ranks from Table 4 of
`python -m askcode.summary`. If no such question exists, say so. In one sentence each,
say why you think each search won.

Meaning search ranked q01 higher than word search (rank 1 with meaning, rank 3 with
words): the question's words (status, codes, error, message) appear in many functions, so
word search put resolve_redirects and Response.ok first, while the embedding matched the
question's meaning, raising an error for bad status codes, to raise_for_status. Meaning
search also found q08 at rank 1 where word search missed it, because "hash algorithms for
digest authentication" is close in meaning to build_digest_header even though the
question's other words point at connection code. No question was ranked higher by word
search than by meaning search: every function word search found, meaning search ranked
the same or higher, and both searches missed q05 and q06.

## 5. Your decision rule (Step 8)

One rule for this codebase: when would you paste everything, and when would you search?
Cite the measured cost and the measured correct count of both designs.

Rule: for this codebase I would search by default and paste everything only when a
small number of answers must be right. Pasting the whole codebase was correct on 10 of 10
questions but cost $0.1104 for 549,348 input tokens, about $0.011 per question, while
searching the top 3 by words cost $0.0054 for 24,295 input tokens but was correct on only
5 of 10, and 4 of its 5 misses were retrieval failures. Meaning search found the right
function for 7 of 9 answerable questions against 5 of 9 for words (retrieval only; I did
not run the AI on its results), and the gold run was correct on 10 of 10 for $0.0021, so
better retrieval is the cheap path to whole-codebase accuracy. I would use meaning search
for everyday questions and paste everything for a few high-stakes ones, where the 20 times
higher cost is still only cents.
