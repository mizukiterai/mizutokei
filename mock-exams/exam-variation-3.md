# Claude Certified Architect — Mock Exam, Form C (Advanced)

**Time limit:** 90 minutes · **Total:** 100 points · **Passing:** 75
Do not open `answer-keys.md` until you have finished.

---

## Section 1 — Multiple choice (25 × 2 pts = 50 pts)

Choose the single best answer.

**A1.** Two parallel requests share an identical 30K-token prefix and are fired at the
exact same moment. What happens to caching?

- A. Both read from cache
- B. Both pay full price — a cache entry is only readable after the first response begins streaming
- C. The second request errors
- D. One request is queued behind the other automatically

**A2.** To eliminate first-request cache-miss latency at startup, the modern technique is
to send a request with:

- A. `max_tokens: 1`
- B. `max_tokens: 0` (prefill-only; writes the cache, returns immediately)
- C. `stream: true` and discard the result
- D. A duplicate of the real request

**A3.** `max_tokens: 0` cache pre-warming is rejected in combination with which of the
following?

- A. A `system` field
- B. `stream: true`, `thinking` enabled, `output_config.format`, or a forced `tool_choice`
- C. A `messages` array
- D. The `anthropic-version` header

**A4.** On a 3,000-token prefix, prompt caching will silently NOT cache on which model
due to the minimum-cacheable-prefix threshold?

- A. `claude-sonnet-4-6` (2048-token minimum)
- B. `claude-fable-5` (2048-token minimum)
- C. `claude-opus-4-8` (4096-token minimum)
- D. `claude-sonnet-4-5` (1024-token minimum)

**A5.** A fork operation (summarization sub-call) rebuilds `system` with a one-character
difference from the parent. The consequence is:

- A. The fork still reads the parent's cache
- B. The fork misses the parent's cache entirely and pays full price
- C. Only the tools cache is lost
- D. A 400 error

**A6.** With `thinking` disabled on Opus 4.8, a known behavior is that the model may:

- A. Refuse the request
- B. Write longer reasoning into the visible response; mitigate with adaptive thinking or a final-answer-only instruction
- C. Ignore the system prompt
- D. Return empty content

**A7.** On `claude-fable-5`, the raw chain of thought is:

- A. Always returned in full
- B. Never returned; `display: "summarized"` gives a summary, `"omitted"` (default) yields empty thinking text
- C. Returned only with a beta header
- D. Returned as `redacted_thinking` blocks

**A8.** When continuing a conversation on the **same** Fable 5 model, thinking blocks
(including empty-text ones) must be:

- A. Stripped before sending
- B. Passed back exactly as received; the API rejects modified blocks
- C. Summarized client-side
- D. Replaced with placeholders

**A9.** A Fable 5 thinking block replayed to a **different** model is:

- A. Rejected with a 400
- B. Dropped from the prompt before pricing (typically silently, unbilled)
- C. Billed at double rate
- D. Converted to a text block

**A10.** Task Budgets (beta) differ from `max_tokens` because:

- A. They are a hard per-response ceiling the model can't see
- B. They tell the model its budget for a full agentic loop; the model sees a countdown and self-moderates
- C. They only apply to streaming
- D. They replace `effort`

**A11.** The minimum `task_budget.total` value is:

- A. 1,024 tokens
- B. 20,000 tokens
- C. 64,000 tokens
- D. There is no minimum

**A12.** In the cache invalidation hierarchy, which change invalidates **everything**
(tools, system, and messages)?

- A. Toggling `thinking` on/off
- B. Changing `tool_choice`
- C. Adding, removing, or reordering a tool definition
- D. Changing the last user message

**A13.** A single agentic turn appends 30 tool_use/tool_result blocks. The next request's
breakpoint silently misses the prior cache because:

- A. The TTL expired
- B. The 20-block lookback window was exceeded; add an intermediate breakpoint mid-turn
- C. Tools can't be cached
- D. The model changed

**A14.** Programmatic tool calling (PTC) reduces token cost primarily by:

- A. Compressing the system prompt
- B. Running tool calls in a script so intermediate results stay out of Claude's context
- C. Using a cheaper model for tools
- D. Disabling thinking

**A15.** Tool search is preferred over loading all tool schemas upfront because it:

- A. Appends discovered schemas (preserving cache) rather than swapping the tool set
- B. Removes the need for tool descriptions
- C. Runs tools server-side
- D. Doubles the context window

**A16.** A `claude-fable-5` request declines mid-stream (after partial output) with a
refusal. The correct handling is:

- A. Treat the partial output as the final answer
- B. Discard the partial output (it is billed, but incomplete) and handle the refusal
- C. The partial output is never billed
- D. Automatically retry on the same model

**A17.** For the server-side `fallbacks` parameter, the supported fallback model target
at launch is:

- A. `claude-haiku-4-5`
- B. `claude-opus-4-8`
- C. `claude-sonnet-4-5`
- D. Any model you name

**A18.** Sticky routing for server-side fallbacks means:

- A. Every request always hits the requested model
- B. After a conversation falls back, later non-streaming requests are served by the fallback model for ~1 hour
- C. The fallback is permanent
- D. Streaming requests are pinned for 24 hours

**A19.** On Managed Agents, to generate a pull request you need, in addition to a
`github_repository` resource mount:

- A. Nothing else — the mount can open PRs
- B. The GitHub MCP server (the mount is filesystem + git only)
- C. A second environment
- D. A custom `open_pr` tool only

**A20.** A vault `environment_variable` credential is exposed to the sandbox as:

- A. The real secret value in an env var
- B. An opaque placeholder; the real value is substituted at egress for allowed hosts
- C. A file under `/memories`
- D. A tool definition

**A21.** Which mechanism keeps a third-party API secret entirely host-side when a vault
doesn't fit (e.g., self-hosted sandboxes)?

- A. Putting the key in the system prompt
- B. A custom tool: the agent emits `agent.custom_tool_use`, your orchestrator calls the API and returns the result
- C. The Files API
- D. The `metadata` field

**A22.** When draining a Managed Agents session stream, you should break on:

- A. Any `session.status_idle`
- B. `session.status_idle` with a terminal `stop_reason`, or `session.status_terminated`
- C. The first `agent.message`
- D. `span.model_request_start`

**A23.** The SSE event stream for a Managed Agents session has no replay. On reconnect,
the robust pattern is to:

- A. Resume the stream from "now" and accept the gap
- B. Fetch event history via `events.list()` and dedupe by event ID while tailing the live stream
- C. Delete and recreate the session
- D. Switch to webhooks only

**A24.** A code-review harness on Opus 4.8 that says "only report high-severity issues"
shows lower measured recall than the prior model. The likely cause and fix:

- A. A capability regression; downgrade the model
- B. The model follows the severity filter more literally; instruct it to report everything and filter downstream
- C. The model can't review code; add more tools
- D. Increase `max_tokens`

**A25.** Which statement about Managed Agents availability across providers is correct?

- A. Managed Agents works on Amazon Bedrock, Vertex AI, and Microsoft Foundry
- B. Managed Agents is available on the first-party API and Claude Platform on AWS, but not on Bedrock/Vertex/Foundry
- C. Managed Agents is only available on Bedrock
- D. Managed Agents requires a self-hosted sandbox everywhere

---

## Section 2 — Multiple response (8 × 3 pts = 24 pts)

Select **all** correct options. No partial credit.

**B1.** Which are true about the cache invalidation tiers? (Select all)

- A. Changing `tool_choice` keeps the tools+system cache intact
- B. Toggling `thinking` keeps the tools+system cache but invalidates messages downstream
- C. A model switch forces a full rebuild
- D. Changing message content invalidates the tools cache

**B2.** Which are correct about Fable 5 refusal billing? (Select all)

- A. A pre-output refusal (empty content) is not billed at all
- B. A mid-stream refusal bills the already-streamed output
- C. With server-side fallbacks, a declined-before-output attempt isn't billed; the rescue bills at the fallback model's rates
- D. All refusals are always billed in full

**B3.** Which are valid agent-specific caching workarounds? (Select all)

- A. Append a `role:"system"` message instead of editing the top-level system prompt
- B. Spawn a subagent on a cheaper model rather than switching the main loop's model
- C. Use tool search to append schemas rather than swapping the tool set
- D. Re-create the agent each turn to refresh the cache

**B4.** Which are true about Managed Agents environments? (Select all)

- A. `config.type` is `cloud` or `self_hosted`
- B. Environment names must be unique (409 on duplicate)
- C. `unrestricted` networking allows full egress (except a legal blocklist)
- D. Self-hosted sandboxes support `environment_variable` vault credentials

**B5.** Which are true about high-resolution vision on Opus 4.7+? (Select all)

- A. Max image resolution increased to 2576px on the long edge
- B. Returned coordinates map 1:1 to actual image pixels
- C. Full-resolution images can use meaningfully more image tokens
- D. It requires a special beta header to enable

**B6.** Which are correct about prompt caching economics and verification? (Select all)

- A. 1-hour TTL writes cost ~2× and need more reads to pay off than 5-minute TTL
- B. `input_tokens` is the uncached remainder only
- C. Total prompt size = `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`
- D. A non-zero `cache_creation_input_tokens` proves a cache read occurred

**B7.** Which are correct uses of mid-conversation system messages
(`role:"system"` in `messages`)? (Select all)

- A. They preserve the cached history prefix
- B. They are a prompt-injection-safe operator channel
- C. They must follow a user message and cannot be `messages[0]`
- D. They are supported on every model with no possibility of a 400

**B8.** Which are true about choosing between surfaces for an agent? (Select all)

- A. Use Managed Agents when you want Anthropic to run the loop and host the tool sandbox
- B. Use Claude API + tool use when you host the compute / custom tool runtime
- C. A single LLM call suffices for classification/summarization/extraction
- D. Always build an agent regardless of task complexity

---

## Section 3 — Scenario design (3 questions, ~8.6 pts each = 26 pts)

Answer in a few sentences each. Name specific features/parameters.

**C1. (Caching architecture under load)**
A RAG service has a 25K-token shared instruction+few-shot preamble and a per-user
retrieved-document block (varies per request), followed by the user's question. Traffic
is bursty with multi-minute idle gaps. Describe your breakpoint strategy, TTL choice,
whether to pre-warm, and the one ordering rule that must hold for any of it to work.

**C2. (Fable 5 production hardening)**
You're deploying `claude-fable-5` for a security-tooling assistant where benign requests
occasionally trip safety classifiers. Describe: (a) how you detect a refusal in code,
(b) the recommended opt-in resilience you'd ship by default, (c) two operational
requirements (retention, fallback rate-limit sizing) you must plan for.

**C3. (Multi-surface deployment trade-off)**
A regulated enterprise must run on AWS infrastructure with IAM-based access control, and
wants Managed Agents plus server-side tools with same-day feature parity. Compare
**Claude Platform on AWS** vs **Amazon Bedrock** for this requirement, state which you'd
choose and why, and note one capability that is NOT available on the option you reject.

---

*End of Form C. Score with `answer-keys.md`.*
