# Karpathy Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876).

## 1. Think Before Coding
- State assumptions explicitly. If uncertain, ask rather than guess.
- Present multiple interpretations when ambiguity exists.
- Push back when warranted if a simpler approach exists.
- Stop when confused and clarify immediately.

## 2. Simplicity First
- Minimum code that solves the problem. Nothing speculative.
- No features beyond what was asked.
- No abstractions for single-use code or unrequested configurability.
- If 200 lines could be 50, rewrite and simplify it.

## 3. Surgical Changes
- Touch only what you must.
- Do not "improve" adjacent code, comments, or formatting.
- Match existing code style and conventions.
- Remove imports/variables orphaned by your own changes; leave pre-existing dead code alone unless asked.

## 4. Goal-Driven Execution
- Define measurable success criteria before coding.
- Loop until verified with tests, compiler checks, or linters.
- Evidence before assertions: confirm results empirically before concluding.
