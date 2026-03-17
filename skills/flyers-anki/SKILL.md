---
name: flyers-anki
description: Build and maintain Cambridge Young Learners (Pre A1 Starters, A1 Movers, A2 Flyers) Anki decks, including wordlist extraction from the official PDF, dictation deck generation, full-vocabulary deck generation, dual-accent audio fields, and related review PDFs. Use when: creating or updating the Flyers/Starters/Movers wordlists, generating `.apkg` packages, exporting review PDFs/CSVs, refining dictation-vs-full-vocab scope, or continuing the existing `flyers_anki/` project in this workspace.
---

# Flyers Anki

## Overview

Use this skill for the `flyers_anki/` project in the workspace. It covers three connected tasks:

1. Wordlist extraction and classification from the Cambridge PDF
2. Dictation deck generation
3. Full-vocabulary deck generation

This skill assumes the project source of truth lives in:

- `/root/.openclaw/workspace/flyers_anki`

## Workflow

### 1. Start from the existing project files

Use the existing project instead of re-creating structure from scratch.

Key folders:

- `flyers_anki/source/` — source PDFs/text
- `flyers_anki/data/` — extracted/classified CSVs + review PDFs
- `flyers_anki/specs/` — product/spec files
- `flyers_anki/scripts/` — generation scripts
- `flyers_anki/out/` — generated `.apkg`, CSV, JSON outputs

### 2. Check which output is being requested

Common requests:

- **Update wordlists** → use the wordlist scripts/specs
- **Rebuild dictation deck** → use dictation scripts/specs
- **Rebuild full vocabulary deck** → use full-vocab scripts/specs
- **Adjust scope/rules first** → update the relevant spec before rebuilding

### 3. Read the relevant spec before changing outputs

Read only the spec you need:

- `references/wordlist-spec.md`
- `references/dictation-deck-spec.md`
- `references/full-vocab-deck-spec.md`
- `references/dual-accent-spec.md`

If you need the operational workflow, also read:

- `references/usage.md`

### 4. Use the bundled scripts when possible

Primary scripts:

- `scripts/build_wordlists.py`
- `scripts/build_dictation_template.py`
- `scripts/build_dictation_full.py`
- `scripts/build_full_vocab_full.py`

If a script already does the requested job, run it instead of rewriting the workflow manually.

### 5. Publish outputs

Typical final outputs:

- `.apkg`
- `.csv`
- review `.pdf`

If the user wants downloads, copy final artifacts to:

- `/var/www/html/`

and give them a full `https://down.beizao.com/...` link when appropriate.

## Current project conventions

### Wordlists

There are two main wordlist modes:

1. **Full vocabulary**
   - based on the combined alphabetic vocabulary list
   - currently tracked via `smf_full_vocab.csv`

2. **Dictation selection**
   - narrowed from the full vocabulary list
   - currently tracked via `smf_selected_dictation.csv`

### Deck types

#### Dictation deck

- front side: no Chinese hint, no answer
- default autoplay: UK audio
- buttons: UK / US
- back side: word, Chinese, level, topic, EN example, ZH example
- default training accent note appears on the answer side

#### Full vocabulary deck

- front side: word + audio buttons + image placeholder
- no Chinese on the front
- back side: Chinese, examples, level, topic, audio buttons
- no “default training accent” note on the back

## Notes

- Current audio generation uses gTTS, producing local MP3s that are bundled into `.apkg`
- Review PDFs are generated from HTML using headless Chrome
- Prefer updating the existing pipeline rather than introducing a second parallel pipeline
