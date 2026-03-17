# Usage

## What this coach uses

This coach runs from an existing structured speaking bank JSON.

Current worked example:

- `../flyers-speaking-bank/references/test1-speaking-bank.json`

## Common ways to invoke

### Full bank

- `Use go-flyers-test1-speaking and start practice.`
- `Start Test1 speaking practice.`
- `Practice Test1 full test.`

### Single part

- `Use go-flyers-test1-speaking and practice part_3 only.`
- `Practice Test1 Part 3 only.`
- `Practice Tell the story from Test1.`
- `Practice Test1 Part1 only.`
- `Use go-flyers-test1-speaking and practice part1 only.`
- `Practice Test1 part1.`

### From a specific exchange

- `Use go-flyers-test1-speaking and continue from p2_ex_003.`

## Shortcut aliases

The coach should accept these shorthand forms:

- `part0` = `part_0`
- `part1` = `part_1`
- `part2` = `part_2`
- `part3` = `part_3`
- `part4` = `part_4`

For current Flyers speaking banks:

- `part0` = Opening / warm-up
- `part1` = Find the differences
- `part2` = Information exchange
- `part3` = Tell the story
- `part4` = Personal questions

## Expected runtime behavior

- If a bank and part are specified, run only that part.
- If only a bank is specified, run the full bank in order.
- If the child is wrong, use the bank's priority answer first when available.
- If the child stops early, output `Session Summary` and `Session Record`.
