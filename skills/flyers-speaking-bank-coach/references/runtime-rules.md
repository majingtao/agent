# Runtime Rules

## 1. Selection order

When the user wants practice:

1. resolve the bank
2. resolve the part if specified
3. resolve the exchange if specified
4. run only that scope

## 2. Part execution

For each part:

- read `instructions`
- first complete the main prompt flow from `exchanges` or `story_frames`
- do not let the extra `questions` interrupt or replace the main scripted dialogue
- after the main prompt flow is finished, continue with the part-level `questions` list as extra follow-up practice
- go through the `questions` list in order until all questions in that part have been used
- for `information_exchange`, handle the child-question stage differently: do not force strict order, and treat the target questions as a coverage set
- do not jump to other parts unless requested

## 3. Answer teaching order

If the child is wrong or cannot answer:

1. use `answer_support.priority_answer` first if present
2. if the priority answer is a slot value, use the child's own real information
3. if there is no usable priority answer, use the fallback rule
4. keep the correction short and child-friendly

If the child answers correctly, continue normally.
In both cases, do not stop the part early just because one answer was completed.
Keep going through the part's `questions` list until all extra questions have been asked.

For part-level `questions` that do not have their own stored answer:

- generate a short A2-level reference answer that matches the bank context
- use it only as extra teaching support for the added question
- do not change the original main-dialogue answers in `exchanges` or `story_frames`

## 4. Information exchange special mode

For `information_exchange`:

- examiner-to-child questions may follow the bank order
- child-to-examiner questions should not require strict order
- treat the expected child questions as a coverage set
- do not show the child exact prompt hints for what to ask next
- a child question counts as correct if it matches one of the intended information points, even if the order is different
- the goal is to cover the full question set, not to force a memorized sequence
- do not end the child-question stage early
- only finish this stage after all target information points in the set have been covered
- for current Test1/Test2-style cards, this means all 5 target questions must be covered before the part can end

## 5. Story parts

For `tell_the_story`:

- each picture / story frame should first get one main child sentence
- first ask the child to look at the picture and describe it
- do not read `teacher_setup` aloud as the child's model answer at the start
- do not start a frame by giving the full standard sentence
- use `teacher_setup` only as internal guidance or very light scene framing
- then use `support_questions` and part-level `questions` only as expansion after the child has tried the main sentence
- use `support_questions` only if needed
- only give a full model sentence after the child has tried and still needs help, or is clearly wrong, or cannot continue
- do not over-scaffold too early

## 6. Part priority rules

For `personal_questions` and other exchange-based parts:

- finish the main `exchanges` first
- only after the main exchange flow is complete, use the part-level `questions` as supplementary practice
- do not let supplementary `questions` replace the main dialogue

## 7. Single-part mode

If the user asked for one part only:

- stop after that part
- do not auto-continue into the next part

## 8. End output

Do not output `Session Summary` or `Session Record` by default.
If the session ends, end naturally.
Only provide a summary or record if the user explicitly asks for it.
