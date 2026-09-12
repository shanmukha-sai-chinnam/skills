---
name: karpathy-guidelines
description: Use when writing, reviewing, refactoring, or planning code changes to enforce simplicity, surgical edits, clear assumptions, and goal-driven verification loops.
---

# Karpathy Guidelines

Behavioral guidelines to eliminate common LLM coding pitfalls, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on AI coding weaknesses.

> **Tradeoff:** These guidelines bias toward caution, simplicity, and verification over raw typing speed. For trivial tasks, use pragmatic judgment.

---

## The Four Core Principles

```
  ┌─────────────────────────────────────────────────────────────┐
  │ 1. THINK BEFORE CODING                                      │
  │    State assumptions. Ask before guessing. Surface tradeoffs.│
  └──────────────────────────────┬──────────────────────────────┘
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 2. SIMPLICITY FIRST                                         │
  │    Minimum code that solves the problem. No speculative bloat.│
  └──────────────────────────────┬──────────────────────────────┘
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 3. SURGICAL CHANGES                                         │
  │    Touch only what you must. Clean up only your own mess.   │
  └──────────────────────────────┬──────────────────────────────┘
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 4. GOAL-DRIVEN EXECUTION                                    │
  │    Define measurable criteria. Loop until verified.         │
  └─────────────────────────────────────────────────────────────┘
```

---

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before making modifications or writing code:
- **State assumptions explicitly:** If uncertain about API behaviors, types, or user intent, ask rather than guess.
- **Present alternatives:** If multiple valid interpretations exist, outline them clearly—never pick silently.
- **Surface tradeoffs:** Identify performance, complexity, or architectural consequences early.
- **Push back constructively:** If a simpler approach or existing utility solves the problem, propose it.
- **Stop when confused:** If instructions or existing code seem contradictory, pause and clarify immediately.

---

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- **No speculative features:** Implement only what was directly requested.
- **No premature abstractions:** Do not create generic helper classes or wrappers for single-use logic.
- **No unrequested configurability:** Avoid adding flags, options, or environment variables unless explicitly instructed.
- **No defensive code for impossible states:** Handle expected edge cases, not hypothetical universe failures.
- **Cut line bloat:** If an implementation takes 200 lines and could be done cleanly in 50, rewrite it before presenting it.

> **The Senior Engineer Test:** *"Would a senior engineer review this and flag it as overengineered?"* If yes, strip it down.

---

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

### When Editing Existing Code:
- **Do not touch adjacent code:** Never reformat, "clean up", or rephrase comments outside your target block.
- **Respect established style:** Match existing conventions, idioms, and naming styles—even if you prefer another.
- **Preserve working code:** Do not refactor unrelated code that happens to sit near the lines you are changing.
- **Report unrelated issues:** If you discover unrelated dead code or bugs, document them for the user—do not delete or fix without asking.

### Managing Orphans:
- **Remove your own debris:** Delete any imports, variables, or functions that *your changes* made obsolete.
- **Leave pre-existing dead code alone:** Unless explicitly asked to clean up technical debt.

> **The Precision Test:** Every modified line in the git diff must trace directly to the user's objective.

---

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform fuzzy, imperative requests into concrete, verifiable milestones:

| Fuzzy Instruction | Transformed Verifiable Goal |
|---|---|
| "Add input validation" | "Write tests for invalid payloads, then implement validation until tests pass" |
| "Fix the bug" | "Write a reproducing test showing failure, then apply fix until green" |
| "Refactor function X" | "Ensure existing test suite passes before and after the refactoring" |

### The Verification Loop
For multi-step work, formulate an explicit execution plan with verification checkpoints:
```text
1. [Step 1] ──► Verify: [Specific command, test, or check]
2. [Step 2] ──► Verify: [Specific command, test, or check]
3. [Step 3] ──► Verify: [Specific command, test, or check]
```

Strong, measurable success criteria allow autonomous, high-confidence iteration.

---

## Red Flags: STOP and Rethink

If any of these thoughts occur, STOP immediately—you are rationalizing a bad pattern:

| Rationalization | Reality |
|---|---|
| *"While I'm here, I'll clean up this function too."* | Surgical changes rule: Touch only what was asked. Revert unrelated edits. |
| *"Let's build an extensible interface in case they need it later."* | Simplicity first: YAGNI (You Aren't Gonna Need It). Build the simplest working solution. |
| *"I think they probably mean X, I'll just code it that way."* | Think before coding: Never guess silently. State your assumption or ask. |
| *"The code looks correct, so it must work."* | Goal-driven execution: Evidence before claims. Run the test/build and observe the output. |
| *"I'll add error handling for all 10 potential edge cases."* | Avoid speculative handling for impossible conditions. |

---

## Quick Reference

| Phase | Core Question | Action |
|---|---|---|
| **Planning** | *Are my assumptions explicit and requirements clear?* | Clarify ambiguities; propose the simplest viable path. |
| **Drafting** | *Is this the minimum code needed?* | Avoid speculative abstractions and premature configurability. |
| **Editing** | *Are all changed lines strictly necessary?* | Audit git diff; remove orthogonal refactors or formatting churn. |
| **Verifying** | *Can I prove this works with deterministic output?* | Run tests, compilers, or linters; check output before declaring success. |
