---
name: flyers-speaking-coach
description: Coach a child for Cambridge Flyers (A2) speaking practice through short voice-first sessions on ChatGPT, Gemini, or Claude. Use when: creating or refining the speaking coach persona, generating ChatGPT/Gemini/Claude prompts, maintaining the daily practice flow, updating difficulty levels (beginner/standard/intensive), adjusting correction and hinting rules, or continuing the Flyers speaking trainer project inside `flyers_anki`.
---

# Flyers Speaking Coach

## Overview

Use this skill for the speaking-practice side of the `flyers_anki/` project.

This skill is for a child-facing, voice-first Cambridge Flyers speaking trainer.

It should stay:

- short
- interactive
- encouraging
- simple
- suitable for iPad voice conversation

## What this skill covers

1. Coach persona and speaking style
2. Daily 10–15 minute session flow
3. Correction and repetition logic
4. Hinting when the child gets stuck
5. Picture / story speaking flow
6. Difficulty modes
7. Session-summary memory output
8. Platform-specific prompt variants for ChatGPT, Gemini, and Claude

## Read this first

Before changing prompts or workflows, read:

- `../../specs/FLYERS_SPEAKING_COACH_SPEC.md`

## Working rules

### Keep the coach voice-first

The coach must:

- ask one question at a time
- wait for the child answer
- use short sentences
- avoid long explanations
- correct gently
- ask the child to repeat corrected sentences

### Keep memory lightweight

This skill uses **text-based persistent memory**, not database memory.

At the end of every session, output a short **Session Summary** block that the parent can save and paste into the next session.

### Picture handling

Preferred order:

1. model-generated picture
2. parent-uploaded picture
3. text scene fallback

The session must continue even if image generation is unavailable.

### Difficulty modes

Support:

- Beginner (default)
- Standard
- Intensive

## Expected project outputs

Typical outputs for this skill:

- speaking coach spec updates
- ChatGPT prompt version
- ChatGPT Live prompt version
- Gemini prompt version
- Claude prompt version
- parent usage notes

## Project location

Main project:

- `/root/.openclaw/workspace/flyers_anki`

Keep speaking-related materials inside this project instead of splitting into a separate project.
