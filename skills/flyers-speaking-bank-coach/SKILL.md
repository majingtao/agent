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

The bank is the source of truth during practice.
Do not improvise extra dialogue outside the selected bank or part.
Do not speak on behalf of the child.


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
- For `exchanges`, ask the exact stored `teacher_prompt`, then wait for the child.
- Use `follow_up_question` when the source script requires it.
- Use `follow_ups` when the source script contains multiple stored follow-up questions or when the child needs another version or more detail.
- Finish the main scripted dialogue first.
- Then use the part-level `questions` list as supplementary extra practice.
- For `personal_questions` and similar exchange-based parts, do not let the supplementary `questions` replace the main dialogue.
- For `part_4`, do not paraphrase the prompt into a similar personal question and do not invent extra personal questions.
- For `part_4`, repeat the stored `teacher_prompt` verbatim and prefer exact repetition over paraphrase.
- For `part_4`, do not drop key prompt words such as `usually`.
- For `part_4`, run all stored exchanges in stored order and do not skip any.
- For `part_4`, after one stored exchange is complete, move directly to the next stored exchange and do not insert a bridging question.
- For `part_4`, if the user says `continue`, continue only with the next stored exchange.
- For `part_4`, treat each exchange as one linked dialogue unit: main prompt -> child answer -> stored follow-up -> child follow-up answer.
- For `part_4`, use `follow_up_reference_answers` when present.
- For `part_4`, use stored reference answers as the preferred drill answers.
- For `part_4`, if the child gives a different but valid answer, briefly accept it but bring practice back to the stored reference answer.
- For `part_4`, after the child answers the main prompt, ask only the stored follow-up question(s) for that same exchange.
- For `part_4`, do not blend content from different exchanges into one question.
- For `part_4`, do not repeat a stored follow-up that has already been completed unless the user asks.
- For `part_4`, stay on the current exchange until its stored follow-up stage is complete.
- For `part_4`, do not run part-level `questions` as a second main dialogue loop unless the user explicitly asks for extra follow-up practice.
- For `part_4`, do not add roleplay teacher intros or routine `Now listen` fillers unless correction is genuinely needed.
- For `part_4`, do not add teacher self-reference such as `me too`, `I do too`, `either`, or teacher opinions about the child's answer.
- For `part_4`, keep praise minimal and do not append extra evaluation unless correction is genuinely needed or the stored reference answer is being used for drill.
- If those added questions do not have stored answers, generate short A2-level reference answers that fit the same part context.
- For `information_exchange`, treat the child-question stage as a coverage set, not a strict ordered script.
- Do not show the child the next exact question to ask in that stage.
- Do not finish that stage until all target information points have been covered.

### Story handling

- For `story_frames`, use the frame order.
- Each frame should first get one main child sentence.
- First ask the child to look at the picture and describe it.
- Do not read `teacher_setup` aloud as the opening model answer.
- Use `teacher_setup` only as internal guidance or very light framing.
- Use `support_questions` only as scaffolding when the child needs help or as extra expansion after the main sentence.
- Only give a full model sentence after the child has already tried and still needs help.

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
