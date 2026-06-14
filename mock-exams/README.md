# Claude Certified Architect — Mock Exam Pack

Three independent practice exams for the **Claude Certified Architect** certification.
Use them to self-assess your readiness to design, build, and operate production
applications on the Claude Developer Platform.

## What this pack contains

| File | Purpose |
|------|---------|
| `exam-variation-1.md` | Full mock exam, Form A (question sheet only) |
| `exam-variation-2.md` | Full mock exam, Form B (question sheet only) |
| `exam-variation-3.md` | Full mock exam, Form C (question sheet only) |
| `answer-keys.md` | Answer keys + explanations for all three forms |

Each form has the same structure so your scores are comparable across attempts:

- **Section 1 — Multiple choice (25 questions, 2 pts each = 50 pts)**
- **Section 2 — Multiple response / "select all that apply" (8 questions, 3 pts each = 24 pts)**
- **Section 3 — Scenario design (3 short-answer questions, ~8.6 pts each = 26 pts)**
- **Total: 100 points. Passing score: 75.**

## Domains covered (blueprint)

The questions are distributed across the architect competency areas:

1. **Model selection & platform fundamentals** — model family, context windows, pricing tiers, the Messages API surface.
2. **Prompt engineering & context design** — system prompts, structured outputs, prompt caching.
3. **Tool use & agents** — user-defined vs. server tools, the agentic loop, tool-runner vs. manual loop, Managed Agents.
4. **Reliability & operations** — streaming, error handling, retries, rate limits, batches.
5. **Context management at scale** — compaction, context editing, memory, long-running agents.
6. **Cost & performance optimization** — caching economics, effort/thinking, token counting, model routing.
7. **Safety, governance & deployment** — refusals, data retention, deployment surfaces (first-party / AWS / Bedrock / Vertex / Foundry).

## How to take a mock exam

1. Set a 90-minute timer. Open only one variation file.
2. Write your answers on paper or in a scratch file — don't peek at `answer-keys.md`.
3. Score yourself against the key. Anything below 75 → review the linked domain and retake a different form.
4. Forms increase slightly in difficulty: Form A is foundational, Form B is intermediate, Form C is the hardest (architecture trade-offs, edge cases).

## A note on accuracy

These questions reflect the current Claude platform: the **Claude 5 (Fable/Mythos)**,
**Opus 4.x**, **Sonnet 4.6**, and **Haiku 4.5** model families; adaptive thinking
and the `effort` parameter; prompt caching; tool use and Managed Agents; and the
Messages API. They are study aids written to mirror the style and rigor of the real
exam — they are **not** official Anthropic exam content.
