# Agentic AI Lead — Assessment

## Overview

This repository contains an IT helpdesk triage agent built by a junior developer. Your task is to analyze the code, review design decisions, and implement a feature.

**You do not need to run the code.** No API keys are required. Part 1 can be answered by reading the source files. Part 2 requires writing code but not executing it.

---

## Deliverables

1. **`solution.md`** — Responses to Q1-Q2 (Part 1)
2. **`decisions.md`** — Design review (Part 1)
3. **Modified `src/` files** — Confidence mechanism (Part 2)

---

# Part 1 — Analysis (~35 min)

### Section A — Code Analysis

#### Q1: Retrieval Fix
For ticket TKT-001 ("error code 619"), the model classifies correctly but recommends generic VPN steps instead of the specific fix for error 619.
- The developer proposes increasing `top_k` from 3 to 10. Is this effective? What is the actual root cause?
- Propose your fix. You may modify `retrieval.py` or describe the change. Keep it minimal — what is the **smallest** change that solves the problem?


#### Q2: Code Review Triage
A junior developer wrote this codebase and our automated reviewer flagged six issues. You are performing the PR review. For each flagged issue, state whether it is a **real bug that must be fixed** or **acceptable as-is for this codebase**, and explain why in one sentence.

| # | Flagged Issue | File |
|---|---------------|------|
| A | Conversation history shared across tickets | `main.py` |
| B | `_prune_history` uses naive slice deletion | `agent.py` |
| C | `response.content[0].text` accessed without type check | `agent.py` |
| D | No retry logic on `messages.create()` | `agent.py` |
| E | Tool dispatch uses `if` instead of a registry | `tools.py` |
| F | Tool inputs accessed via `params.get()` without Pydantic validation | `tools.py` |


### Section B — Design Review

#### `decisions.md`

Review the **six design decisions** below. For each, state whether you **Agree**, **Disagree**, or **Partially Agree** with the decision, and explain in one sentence. If you disagree, add one sentence describing what you would change.

| # | Decision | Where |
|---|----------|-------|
| 1 | History pruning uses naive slice deletion | `agent.py` `_prune_history` |
| 2 | The regex parser extracts `FIELD: value` pairs from model output | `parser.py` |
| 3 | The system prompt is stored as a Python constant in `prompts.py` | `prompts.py` |
| 4 | No retry logic on `messages.create()` calls | `agent.py` |
| 5 | `response.content[0].text` is accessed without checking block type | `agent.py` |
| 6 | The audit log uses a module-level mutable list (`_audit_log = []`) | `tools.py` |

**Template** — use exactly this format for each:

```
### Decision N: [title]
**Verdict:** Agree / Disagree / Partially Agree
**Why:** [one sentence]
**Alternative:** [one sentence, only if Disagree or Partially Agree]
```

---

# Part 2 — Implementation (~35 min)

### Task: Add Confidence-Based Human Review

Modify the triage pipeline so that tickets where the agent is not confident are flagged for human review instead of being auto-classified. You may modify any files in `src/`.

**Requirements:**
- Implement a mechanism to determine confidence for each classification
- Tickets with low confidence should be flagged in the output (e.g., `"needs_human_review": true`)
- The mechanism should work reliably in production — consider what signals are trustworthy

**Include a comment block at the top of each changed file** explaining:
- How you determine confidence
- Why you chose this approach over alternatives
- What trade-offs you considered

---

### Format Requirements

- `decisions.md` must use the exact template. No extra sections.
- Conciseness is valued. One sentence per verdict in Q2.
- Implementation: working code preferred, pseudocode acceptable if clearly structured.
- **Comments explaining your reasoning are as important as the code itself.**

---

**Expected Time: 70-75 Minutes**

| Section | Deliverable | Suggested Time |
|---------|-------------|---------------|
| Part 1, Section A | Q1-Q2 in `solution.md` | ~25 minutes |
| Part 1, Section B | `decisions.md` | ~15 minutes |
| Part 2 | Modified `src/` files with confidence mechanism | ~30 minutes |
| Buffer | | ~10 minutes |

---

## Submission

1. Fork this repository to your personal GitHub account.
2. Add `solution.md`, `decisions.md`, and any modified/new files.
3. Create a Pull Request back to this repository.
4. **MANDATORY**: Include your name, email and history in the PR description.
