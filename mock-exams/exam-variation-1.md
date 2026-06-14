# Claude Certified Architect — Mock Exam, Form A (Foundational)

**Time limit:** 90 minutes · **Total:** 100 points · **Passing:** 75
Do not open `answer-keys.md` until you have finished.

---

## Section 1 — Multiple choice (25 × 2 pts = 50 pts)

Choose the single best answer.

**A1.** Every text generation request to Claude — including tool use and structured
outputs — goes through which single API endpoint?

- A. `POST /v1/completions`
- B. `POST /v1/messages`
- C. `POST /v1/chat`
- D. A different endpoint per feature (tools, vision, thinking)

**A2.** A teammate writes `model="claude-sonnet-4-6-20251114"` and gets a 404. What is
the most likely cause?

- A. Sonnet 4.6 has been retired
- B. The model ID should not have a date suffix appended; use `claude-sonnet-4-6`
- C. The request is missing the `anthropic-version` header
- D. Date-suffixed IDs require a beta header

**A3.** Which model is the correct default choice for general production work unless the
user explicitly requests otherwise?

- A. `claude-haiku-4-5`
- B. `claude-fable-5`
- C. `claude-opus-4-8`
- D. `claude-sonnet-4-5`

**A4.** You want to force Claude to return JSON matching a fixed schema. The recommended
mechanism is:

- A. Prefill the assistant turn with `{`
- B. The deprecated top-level `output_format` parameter
- C. `output_config: {format: {type: "json_schema", schema: ...}}`
- D. A regex post-processor on the text response

**A5.** Prompt caching is fundamentally a:

- A. Semantic similarity match on request content
- B. Prefix match on the exact rendered bytes up to a `cache_control` breakpoint
- C. Hash of the user's final message only
- D. Cache of model weights per organization

**A6.** The render order that determines the cacheable prefix is:

- A. `messages` → `system` → `tools`
- B. `system` → `messages` → `tools`
- C. `tools` → `system` → `messages`
- D. Whatever order you pass the fields in the request body

**A7.** Putting `datetime.now()` into your system prompt on every request will:

- A. Improve cache hit rate
- B. Invalidate the cache on every request
- C. Have no effect on caching
- D. Cause a 400 error

**A8.** Which is the correct way to enable extended reasoning on `claude-opus-4-8`?

- A. `thinking: {type: "enabled", budget_tokens: 8000}`
- B. `thinking: {type: "adaptive"}`
- C. `temperature: 0` with a "think step by step" prompt
- D. `reasoning: true`

**A9.** On `claude-opus-4-8`, sending `thinking: {type: "enabled", budget_tokens: N}`
results in:

- A. A successful request that caps thinking at N tokens
- B. A 400 error — fixed thinking budgets are removed on this model
- C. A silent fallback to adaptive thinking
- D. A 429 error

**A10.** The `effort` parameter controls thinking depth and overall token spend. It is
placed:

- A. At the top level of the request
- B. Inside `output_config`
- C. Inside `thinking`
- D. In a beta header

**A11.** A `tool_result` block must always include:

- A. The `is_error` field
- B. A matching `tool_use_id`
- C. The original tool's `input_schema`
- D. A `cache_control` marker

**A12.** When Claude wants to call a tool, the response `stop_reason` is:

- A. `end_turn`
- B. `tool_use`
- C. `pause_turn`
- D. `max_tokens`

**A13.** Which is a **server-side** tool that runs entirely on Anthropic's infrastructure?

- A. A custom `get_weather` function you defined
- B. Code execution
- C. The client-side bash reference implementation
- D. A local MCP stdio server

**A14.** The Batches API processes requests asynchronously at what discount versus
standard pricing?

- A. 10%
- B. 25%
- C. 50%
- D. 90%

**A15.** A non-streaming request with a very large `max_tokens` (e.g. 100K) is risky
primarily because:

- A. It always returns a 413
- B. Idle HTTP connections can time out before the response completes
- C. Large outputs are not billed
- D. `max_tokens` above 16K is rejected

**A16.** The Anthropic SDKs automatically retry which errors with exponential backoff?

- A. All 4xx errors
- B. 400 and 401
- C. 408, 409, 429, and ≥500
- D. None — you must implement retries yourself

**A17.** Which response field confirms a prompt-cache hit?

- A. `usage.cache_read_input_tokens`
- B. `usage.output_tokens`
- C. `stop_reason`
- D. `usage.input_tokens`

**A18.** For a chat UI that should display tokens as they are produced, you should:

- A. Poll the Batches API
- B. Use streaming (`messages.stream()`)
- C. Set `max_tokens: 0`
- D. Use the Files API

**A19.** In a multi-turn conversation, the Messages API is:

- A. Stateful — the server remembers prior turns
- B. Stateless — you must send the full history each request
- C. Stateful only when caching is enabled
- D. Stateful only for the first 10 turns

**A20.** Which model is the most cost-effective choice for a simple, high-volume
classification task?

- A. `claude-opus-4-8`
- B. `claude-fable-5`
- C. `claude-haiku-4-5`
- D. `claude-opus-4-7`

**A21.** To count tokens accurately for a Claude prompt you should:

- A. Use `tiktoken`
- B. Use the `count_tokens` endpoint with the same model ID
- C. Divide character count by 4
- D. Read `usage.input_tokens` from a prior unrelated request

**A22.** Managed Agents requires which mandatory two-step flow?

- A. Session first, then Agent
- B. Agent (created once) → Session (every run)
- C. Environment → Vault only
- D. Tool → Skill

**A23.** In Managed Agents, where do `model`, `system`, and `tools` live?

- A. On the session
- B. On the environment
- C. On the agent object
- D. On the vault

**A24.** A request returns HTTP 200 with `stop_reason: "refusal"`. Before reading
`response.content[0]`, you should:

- A. Retry immediately with the same prompt
- B. Check `stop_reason` and handle the refusal (content may be empty)
- C. Assume the content is valid JSON
- D. Switch to a smaller model automatically

**A25.** Which deployment surface offers Anthropic-operated, same-day API parity
(including Managed Agents) with AWS-native IAM and billing?

- A. Amazon Bedrock
- B. Google Vertex AI
- C. Claude Platform on AWS
- D. Microsoft Foundry

---

## Section 2 — Multiple response (8 × 3 pts = 24 pts)

Select **all** correct options. No partial credit.

**B1.** Which of the following will silently invalidate a prompt cache? (Select all)

- A. A `uuid4()` embedded early in the system prompt
- B. `json.dumps()` without sorted keys in the cached prefix
- C. Changing the set of tools mid-conversation
- D. Reading `usage.cache_read_input_tokens` from the response

**B2.** Which are valid `stop_reason` values? (Select all)

- A. `end_turn`
- B. `tool_use`
- C. `refusal`
- D. `cache_miss`

**B3.** Which statements about the tool runner (vs. a manual agentic loop) are true?
(Select all)

- A. The tool runner executes your tool functions automatically and loops until done
- B. A manual loop is preferred when you need human-in-the-loop approval before each call
- C. The tool runner generates tool schemas from your function signatures / typed schemas
- D. The manual loop cannot use streaming

**B4.** Which are characteristics of the Batches API? (Select all)

- A. ~50% cost reduction
- B. Most batches finish within an hour (max 24h)
- C. Supports vision, tools, and caching
- D. Results are guaranteed in request order with no `custom_id` needed

**B5.** Which approaches help manage context in a long-running agent? (Select all)

- A. Compaction (server-side summarization near the limit)
- B. Context editing (pruning stale tool results / thinking)
- C. Memory (cross-session persistence)
- D. Lowering `max_tokens` to 1

**B6.** Which are true about `claude-fable-5`? (Select all)

- A. Thinking is always on; an explicit `thinking: {type: "disabled"}` returns 400
- B. Safety classifiers may return `stop_reason: "refusal"`
- C. It requires 30-day data retention (not available under zero data retention)
- D. It is the recommended default for routine "upgrade to the latest" requests

**B7.** When designing a tool surface, you should promote a bash action to a dedicated
tool when you need to: (Select all)

- A. Gate a hard-to-reverse action behind confirmation
- B. Render a custom UI for the action
- C. Mark a read-only action as parallel-safe
- D. Give Claude maximum unconstrained breadth

**B8.** Which placements are correct for `cache_control` breakpoints? (Select all)

- A. On the last block of a large shared system prompt
- B. On the end of the shared prefix when only the final question varies
- C. On the last content block of the most recent turn in a multi-turn chat
- D. On a block containing a per-request timestamp

---

## Section 3 — Scenario design (3 questions, ~8.6 pts each = 26 pts)

Answer in a few sentences each. Name specific features/parameters.

**C1. (Cost & caching)**
A customer support assistant prepends a 40,000-token knowledge base to every request,
followed by a short, varying user question. Volume is steady (many requests per minute).
Describe how you would structure the request to minimize cost, where you'd place the
cache breakpoint, and how you'd verify it's working.

**C2. (Reliability)**
You're shipping a feature that generates long (~60K token) reports. Describe the request
configuration you'd use, the failure modes you must handle, and how the SDK helps.

**C3. (Architecture choice)**
A client wants an agent that edits a GitHub repo, runs the test suite, and opens a pull
request — with Anthropic hosting the execution sandbox. Which platform surface fits,
what objects must you create and in what order, and how is the GitHub credential handled
securely?

---

*End of Form A. Score with `answer-keys.md`.*
