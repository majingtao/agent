---
name: flyers-speaking-bank-coach
description: Coach a child through Cambridge Flyers speaking practice using a structured speaking bank JSON. Use when the user wants to practice a specific bank, test, part, or exchange, and the coach should follow bank instructions, exchanges, story_frames, and priority answers before falling back to generated answers. Do not use for building the bank itself; use flyers-speaking-bank for extraction and bank design.
---

# Flyers Speaking Bank Coach

Use this skill when the task is to run a child speaking practice session from an existing structured speaking bank.

## What this skill does

This skill:

- loads an existing speaking bank
- supports full-bank practice or single-part practice
- follows `parts`, `instructions`, `exchanges`, and `story_frames`
- uses `answer_support.priority_answer` first when the child is wrong or cannot answer
- falls back to generated A2-level answers only when the bank does not provide a usable priority answer
- preserves coaching rules such as grammar checking, short explanations, and repetition

## What this skill does not do

This skill does not:

- extract content from PDFs
- design bank schemas
- build new bank JSON files

Use `flyers-speaking-bank` for that.

## Read these references first

- `../flyers-speaking-bank/references/schema-v3.json` — bank field structure
- `../flyers-speaking-bank/references/banks-index.json` — available banks and parts
- `../flyers-speaking-bank/references/test1-speaking-bank.json` — current real worked bank
- `references/usage.md` — how to invoke this coach with bank / part / exchange selectors
- `references/runtime-rules.md` — how to run sessions from bank data

## Invocation rules

Support these user intents:

- practice the full bank
- practice a specific test
- practice a specific part, such as `part_3`
- continue from a specific exchange

If the user specifies a bank and a part, only run that part.
If the user specifies a bank and no part, run the full bank in part order.

## Runtime rules

### Bank selection

- Resolve the requested bank by `bank_id` first.
- If the user says `Test1`, map it to the matching bank when unambiguous.
- If the bank is ambiguous, ask one short clarification question.

### Part selection

- If the user requests `part_3`, `part3`, or a named part such as `Tell the story`, only run that part.
- Accept shorthand aliases `part0`..`part4` and map them to `part_0`..`part_4`.
- Do not continue into other parts unless the user asks.
- Within the selected part, keep going until the main prompts and the part-level `questions` list have both been used.

### Exchange handling

- Follow `instructions` at the start of the part.
- For `exchanges`, ask the `teacher_prompt`, then wait for the child.
- Use `follow_up_question` when the source script requires it.
- Use `follow_ups` when the child needs another version or more detail.
- Finish the main scripted dialogue first.
- Then use the part-level `questions` list as supplementary extra practice.
- If those added questions do not have stored answers, generate short A2-level reference answers that fit the same part context.
- For `information_exchange`, treat the child-question stage as a coverage set, not a strict ordered script.
- Do not show the child the next exact question to ask in that stage.
- Do not finish that stage until all target information points have been covered.

### Story handling

- For `story_frames`, use the frame order.
- Use `teacher_setup` to frame the picture/story step.
- Use `support_questions` only as scaffolding when the child needs help.

### Error handling

When the child is wrong or cannot answer:

1. check `answer_support.priority_answer`
2. if present and usable, teach that answer first
3. if not present, use `fallback_answer_rule`
4. briefly explain the mistake
5. give the corrected sentence
6. ask the child to repeat it

### Session ending

Do not output `Session Summary` or `Session Record` by default.
When a single requested part is complete, stop there unless the user asks to continue.
If the user wants a summary or record, provide it only on request.
