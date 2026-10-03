# Assignment 2 Report: Ask the Code

Name:
Provider and model:
Prices used (per million tokens, input and output), and the page you found them on:

## Table 1. Finding the right function

Paste Table 1 from `python -m askcode.summary` here, exactly as printed.

## Table 2. Answers

Paste Table 2 from `python -m askcode.summary` here, exactly as printed.

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

## 3. Minimal prompt against five-part prompt (Step 6)

Which prompt did better on right place, and which on correct? Give both numbers for both
prompts. Name one question where the two prompts' replies differed, and say what
differed.

## 4. Word search against meaning search (Step 7)

Name one question meaning search ranked higher than word search, and one question word
search ranked higher than meaning search, with the ranks from Table 4 of
`python -m askcode.summary`. If no such question exists, say so. In one sentence each,
say why you think each search won.

## 5. Your decision rule (Step 8)

One rule for this codebase: when would you paste everything, and when would you search?
Cite the measured cost and the measured correct count of both designs.
