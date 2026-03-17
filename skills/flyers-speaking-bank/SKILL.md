---
name: flyers-speaking-bank
description: Build and maintain a structured Cambridge Flyers speaking question bank from official PDFs, images, transcripts, and teacher-student dialogue materials. Use when extracting speaking tasks from source materials, organizing them into bank/parts/exchanges/story_frames JSON, defining bank schemas, or preparing speaking-bank data for flyers-speaking-coach.
---

# Flyers Speaking Bank

Use this skill when the job is to turn Flyers speaking source materials into structured bank data.

## What this skill is for

This skill handles:

- extracting speaking content from PDFs or teacher notes
- organizing official-style teacher/student scripts
- structuring materials into JSON bank files
- separating the bank into parts such as opening questions, find the differences, information exchange, tell the story, and personal questions
- preparing data that can later be consumed by `flyers-speaking-coach`

## What this skill is not for

This skill does not handle:

- child-facing coaching prompts
- live correction rules
- ChatGPT / Gemini / Claude prompt writing

Those belong to `flyers-speaking-coach`.

## Default structure

Prefer this structure for official-style speaking banks:

- `bank`
- `parts`
- `instructions`
- `exchanges`
- `story_frames` when the part is story-based

## Read these references as needed

- `references/schema-v3.json` — current structured JSON schema draft
- `references/banks-index.json` — list of available speaking banks
- `references/test1-speaking-bank.json` — worked example from Test 1 speaking material

## Working rules

- Keep the source meaning faithful.
- Preserve teacher wording when it is part of the test script.
- Keep `student_reference` as a reference answer, not the only acceptable answer, unless the task requires fixed card data.
- For information-gap tasks, mark `acceptable_variations` carefully; many should be `false`.
- For image-based tasks, set image handling to offline/paper if the model does not see the image.
