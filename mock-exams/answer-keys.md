# Answer Keys & Explanations — All Forms

Score each form out of 100. Passing is 75.
Section 1: 2 pts each · Section 2: 3 pts each (all-or-nothing) · Section 3: ~8.6 pts each.

For Section 3, award full marks if your answer hits the key points listed.

---

## Form A (Foundational)

### Section 1

| Q | Ans | Why |
|---|-----|-----|
| A1 | **B** | All generation flows through `POST /v1/messages`; tools/structured outputs/thinking are features of it. |
| A2 | **B** | Use the exact alias `claude-sonnet-4-6` — don't append a recalled date suffix. |
| A3 | **C** | `claude-opus-4-8` is the production default unless the user picks another model. |
| A4 | **C** | Structured outputs via `output_config.format`; `output_format` is deprecated and prefill is removed on current models. |
| A5 | **B** | Caching is a prefix match on exact rendered bytes up to a `cache_control` breakpoint. |
| A6 | **C** | Render order is `tools` → `system` → `messages`. |
| A7 | **B** | A per-request timestamp in the prefix changes the bytes and invalidates the cache every time. |
| A8 | **B** | Adaptive thinking is the on-mode for Opus 4.8. |
| A9 | **B** | Fixed `budget_tokens` is removed on Opus 4.8 → 400. |
| A10 | **B** | `effort` lives inside `output_config`. |
| A11 | **B** | Each `tool_result` must carry the matching `tool_use_id`. |
| A12 | **B** | `tool_use` signals Claude wants a tool executed. |
| A13 | **B** | Code execution runs entirely on Anthropic infrastructure. |
| A14 | **C** | Batches are ~50% cheaper. |
| A15 | **B** | Large non-streaming outputs risk idle-connection HTTP timeouts; stream instead. |
| A16 | **C** | SDK auto-retries 408, 409, 429, ≥500 with backoff. |
| A17 | **A** | `usage.cache_read_input_tokens` > 0 confirms a hit. |
| A18 | **B** | Streaming displays tokens as produced. |
| A19 | **B** | The Messages API is stateless; send full history each request. |
| A20 | **C** | `claude-haiku-4-5` is the cheapest/fastest for simple high-volume tasks. |
| A21 | **B** | Use `count_tokens` with the same model; never `tiktoken`. |
| A22 | **B** | Agent created once → Session every run. |
| A23 | **C** | `model`/`system`/`tools` live on the agent, not the session. |
| A24 | **B** | Check `stop_reason` first; refused content may be empty. |
| A25 | **C** | Claude Platform on AWS is Anthropic-operated with same-day parity + AWS IAM/billing. |

### Section 2

| Q | Ans | Why |
|---|-----|-----|
| B1 | **A, B, C** | All three change/invalidate the prefix; reading a usage field (D) does not. |
| B2 | **A, B, C** | `cache_miss` is not a stop reason. |
| B3 | **A, B, C** | The manual loop can stream (D is false). |
| B4 | **A, B, C** | Results use `custom_id` to correlate; order isn't guaranteed (D false). |
| B5 | **A, B, C** | Lowering `max_tokens` to 1 (D) doesn't manage context. |
| B6 | **A, B, C** | Fable 5 is NOT the default upgrade target (pricing above Opus); D is false. |
| B7 | **A, B, C** | Dedicated tools constrain/gate/render/parallelize; "maximum unconstrained breadth" (D) is the bash argument, not a reason to promote. |
| B8 | **A, B, C** | Never put a breakpoint on a volatile per-request block (D). |

### Section 3 — model answers

**C1 (cost & caching).** Put the 40K-token knowledge base first (stable prefix), the
varying question last. Place a single `cache_control` breakpoint at the **end of the
knowledge base** (the shared portion), not after the question. With steady high traffic,
the default 5-minute ephemeral TTL keeps the cache warm. Verify by checking
`usage.cache_read_input_tokens` > 0 on subsequent requests; if it's zero, audit for
silent invalidators (timestamps/UUIDs, unsorted JSON, varying tool set). Keep the system
prompt frozen.

**C2 (reliability).** Use streaming (`messages.stream()`) with `max_tokens` ~64K (Opus
4.x/Sonnet 4.6 support large outputs but require streaming to avoid HTTP timeouts). Get
the result via `.get_final_message()`/`.finalMessage()`. Handle: rate limits (429),
overload (529), connection drops, `stop_reason == "max_tokens"` (raise the cap / continue).
The SDK auto-retries 429/5xx with backoff and the streaming guard prevents silent
timeout on big non-streamed requests.

**C3 (architecture).** Use **Managed Agents** (Anthropic hosts the execution sandbox).
Create objects in order: **Environment** → **Agent** (once; declares model, system,
tools incl. the **GitHub MCP server** for PR creation) → **Session** (every run; mounts
the `github_repository` resource and attaches a **vault** for MCP credentials). The repo
clone token (`authorization_token`) and MCP OAuth credential never enter the container —
git operations and MCP calls are routed through Anthropic-side proxies that inject the
credential at egress. Flow: edit files → push branch via bash → open PR via the MCP
`create_pull_request` tool.

---

## Form B (Intermediate)

### Section 1

| Q | Ans | Why |
|---|-----|-----|
| A1 | **B** | Tools/structured outputs/server tools are features of `/v1/messages`. |
| A2 | **B** | Adaptive thinking lets Claude decide depth dynamically; no budget to tune. |
| A3 | **B** | `temperature`/`top_p`/`top_k` are removed (400) on Opus 4.8/4.7. |
| A4 | **B** | 5-min TTL write ≈ 1.25× base input. |
| A5 | **A** | Cache reads ≈ 0.1× base input. |
| A6 | **B** | 5-min TTL breaks even at ~2 requests (1.25× + 0.1× < 2×). |
| A7 | **C** | Server tool loop limit → `pause_turn`. |
| A8 | **B** | Re-send user msg + assistant response; server resumes (no "Continue."). |
| A9 | **B** | Append full `response.content` including `tool_use` blocks. |
| A10 | **B** | A `role:"system"` message preserves the cached prefix. |
| A11 | **B** | Editing top-level `system` invalidates the prefix ahead of the whole conversation. |
| A12 | **B** | Max 4 breakpoints. |
| A13 | **C** | 20-block lookback window. |
| A14 | **B** | `client.messages.parse()` validates against the schema. |
| A15 | **C** | Numerical constraints (`minimum`/`maximum`) are unsupported. |
| A16 | **B** | Append `response.content` to preserve compaction blocks. |
| A17 | **B** | Files API references docs by `file_id` across requests. |
| A18 | **B** | `any` = must use at least one tool. |
| A19 | **B** | MCP creds go in a vault attached via `vault_ids`. |
| A20 | **B** | Agent archive is permanent/read-only, no unarchive. |
| A21 | **A** | Set `allow_mcp_servers: true` or list domains in `allowed_hosts`. |
| A22 | **B** | Pin via `{type:"agent", id, version:N}`. |
| A23 | **B** | Server-side `fallbacks` with the `server-side-fallback-2026-06-01` beta. |
| A24 | **B** | Fable 5 needs 30-day retention; ZDR orgs 400 on every request. |
| A25 | **C** | `xhigh` is the best setting for most coding/agentic work on 4.7/4.8/Fable 5. |

### Section 2

| Q | Ans | Why |
|---|-----|-----|
| B1 | **A, D** | System content and message content invalidate system+messages but keep tools cache; tool changes (B) and model switch (C) force a full rebuild. |
| B2 | **A, B, C** | The tool runner (D) is the opposite of "manual loop" use cases. |
| B3 | **A, B, C** | Server tools are declared in `tools` and run server-side; you don't execute them (D false). |
| B4 | **A, B, D** | Sonnet 4.6 is not strictly more capable than Opus 4.8 (C false). |
| B5 | **A, B, C** | Coming from Opus 4.6/older, counts differ (D false). |
| B6 | **A, B, C** | `temperature: 2` (D) is invalid on Fable 5 (sampling params removed) and isn't a fallback. |
| B7 | **A, B, C** | Sessions reference the agent by ID; model/system are on the agent, not inline (D false). |
| B8 | **A, B, C** | Don't blindly max `max_tokens` for every task (D false). |

### Section 3 — model answers

**C1 (agent design, Opus 4.8).** Soften the tool instruction from
`CRITICAL: You MUST use this tool` to a calibrated "Use this tool when…" — current Opus
models follow instructions literally and aggressive language overtriggers. Add explicit
subagent guidance: spawn subagents only for parallel/independent work; for single-file
reads or sequential ops, work directly. Optionally tune `effort` (e.g., `high`) and add a
"don't over-engineer / don't ask on minor decisions" instruction.

**C2 (context at scale).** Combine: **compaction** (server-side summarizes earlier
context near the window limit — append `response.content` each turn to preserve the
compaction block); **context editing** (prunes stale tool results / thinking blocks to
keep the transcript lean); and **memory** (file-based store that persists learnings
across separate sessions). Editing/compaction work within a session; memory is for
cross-session persistence.

**C3 (migration to Opus 4.8).** Required changes: replace
`thinking: {type:"enabled", budget_tokens:8000}` with `thinking: {type:"adaptive"}` (+
optional `output_config.effort`) — fixed budgets 400; remove `temperature: 0.7` (sampling
params 400); remove the final assistant-turn prefill `{"name": "` — prefills 400 — and
replace it with structured outputs (`output_config.format` with a JSON schema) or a
system-prompt instruction. Then update the model string to `claude-opus-4-8`.

---

## Form C (Advanced)

### Section 1

| Q | Ans | Why |
|---|-----|-----|
| A1 | **B** | A cache entry is readable only after the first response begins streaming; simultaneous requests all pay full price. |
| A2 | **B** | `max_tokens: 0` prefill-only writes the cache and returns immediately. |
| A3 | **B** | `max_tokens: 0` is rejected with stream, thinking enabled, `output_config.format`, or a forced `tool_choice`. |
| A4 | **C** | Opus 4.8 minimum cacheable prefix is 4096 tokens → 3K silently won't cache. |
| A5 | **B** | One byte differing in the prefix → full cache miss. |
| A6 | **B** | Disabled thinking on 4.8 can leak reasoning into output; use adaptive or a final-answer-only instruction. |
| A7 | **B** | Raw CoT never returned; summary via `display:"summarized"`, default `"omitted"` = empty thinking text. |
| A8 | **B** | Pass thinking blocks back unchanged on the same model; modified blocks are rejected. |
| A9 | **B** | A Fable 5 thinking block sent to a different model is dropped before pricing (unbilled, typically silent). |
| A10 | **B** | Task Budgets tell the model its loop budget (it sees a countdown); `max_tokens` is the hidden hard ceiling. |
| A11 | **B** | Minimum `task_budget.total` is 20,000. |
| A12 | **C** | Tool definition add/remove/reorder invalidates everything. |
| A13 | **B** | 20-block lookback exceeded; add an intermediate breakpoint. |
| A14 | **B** | PTC keeps intermediate tool results out of context; only final output returns to Claude. |
| A15 | **A** | Tool search appends schemas, preserving the cache. |
| A16 | **B** | Mid-stream refusal bills the partial; discard it and handle the refusal. |
| A17 | **B** | `claude-opus-4-8` is the supported fallback target at launch. |
| A18 | **B** | Sticky routing: ~1 hour, non-streaming, after a fallback occurs. |
| A19 | **B** | PR creation needs the GitHub MCP server; the mount is filesystem + git only. |
| A20 | **B** | `environment_variable` creds appear as an opaque placeholder; substituted at egress for allowed hosts. |
| A21 | **B** | A custom tool keeps the secret host-side via `agent.custom_tool_use` → orchestrator. |
| A22 | **B** | Break on idle-with-terminal-stop-reason or terminated; not every idle (transient). |
| A23 | **B** | Reconnect = fetch `events.list()` history + dedupe by ID while tailing live. |
| A24 | **B** | 4.8 follows severity filters literally; tell it to report everything and filter downstream. |
| A25 | **B** | Managed Agents: first-party + Claude Platform on AWS only (not Bedrock/Vertex/Foundry). |

### Section 2

| Q | Ans | Why |
|---|-----|-----|
| B1 | **A, B, C** | Changing message content does NOT invalidate the tools cache (D false). |
| B2 | **A, B, C** | Not all refusals are billed in full (D false). |
| B3 | **A, B, C** | Re-creating the agent each turn (D) doesn't refresh/help the cache and is an anti-pattern. |
| B4 | **A, B, C** | Self-hosted sandboxes do NOT support `environment_variable` vault creds (D false). |
| B5 | **A, B, C** | High-res vision is automatic on 4.7+, no beta header (D false). |
| B6 | **A, B, C** | `cache_creation_input_tokens` proves a write, not a read (D false). |
| B7 | **A, B, C** | Mid-conversation system messages are model-gated and can 400 on unsupported models (D false). |
| B8 | **A, B, C** | Don't build an agent regardless of complexity — start simple (D false). |

### Section 3 — model answers

**C1 (caching architecture under load).** Place the **first** breakpoint at the end of
the 25K shared preamble (instructions + few-shot) — that's the reusable prefix. The
per-user retrieved-document block and the question come **after** it and get no breakpoint
(they vary). Because traffic is bursty with multi-minute idle gaps that exceed the
5-minute TTL, either re-warm just under the TTL or switch the preamble's breakpoint to
`ttl: "1h"` (write ~2×, but it survives the gaps and pays off across the burst). Pre-warm
at startup with a `max_tokens: 0` request only if first-request latency is user-visible.
The ordering rule that must hold: stable content (frozen system + deterministic
preamble) must physically precede the volatile per-request content — otherwise nothing
caches regardless of markers.

**C2 (Fable 5 production hardening).** (a) Detect by checking
`response.stop_reason == "refusal"` **before** reading `response.content[0]` (content may
be empty pre-output or partial mid-stream). (b) Ship the server-side `fallbacks`
parameter by default (`betas: ["server-side-fallback-2026-06-01"]`,
`fallbacks: [{"model": "claude-opus-4-8"}]`) so a benign-but-flagged request is
transparently re-served instead of failing; on Bedrock/Vertex/Foundry use the client-side
refusal-fallback middleware instead. (c) Operational requirements: the org must meet
**30-day data retention** (ZDR → 400 on every request), and you must **size the fallback
model's rate limits** for expected refusal volume — if the fallback is rate-limited the
preceding refusal is returned instead.

**C3 (multi-surface deployment).** Choose **Claude Platform on AWS**: it is
Anthropic-operated with **same-day API parity**, supports **Managed Agents** and
**server-side tools**, and uses **AWS-native IAM + Marketplace billing** with bare
first-party model IDs (e.g., `claude-opus-4-8`). **Amazon Bedrock** is partner-operated,
has a feature subset, uses `anthropic.`-prefixed model IDs, and does **not** support
Managed Agents or Anthropic server-side tools — so it fails the stated requirement. One
capability NOT available on Bedrock (the rejected option): **Managed Agents** (and
server-side tools generally). Note: self-hosted sandboxes are the one thing Claude
Platform on AWS does not offer — use `cloud` there.

---

## Scoring guide

| Score | Reading |
|-------|---------|
| 90–100 | Exam-ready across all domains. |
| 75–89 | Passing; review the domains where you dropped points. |
| 60–74 | Close — focus on caching mechanics, tool/agent flows, and Fable 5 specifics. |
| < 60 | Re-study fundamentals (Messages API, model selection, prompt caching, tool use) before retaking. |
