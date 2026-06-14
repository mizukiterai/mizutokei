# Claude Certified Architect — Mock Exam, Form B (Intermediate)

**Time limit:** 90 minutes · **Total:** 100 points · **Passing:** 75
Do not open `answer-keys.md` until you have finished.

---

## Section 1 — Multiple choice (25 × 2 pts = 50 pts)

Choose the single best answer.

**A1.** Tools, structured outputs, and server-side tools are best described as:

- A. Separate API products with their own endpoints
- B. Features of the single `POST /v1/messages` endpoint
- C. Only available through Managed Agents
- D. Client-side SDK helpers with no server component

**A2.** Adaptive thinking (`thinking: {type: "adaptive"}`) differs from the old fixed
`budget_tokens` model because:

- A. It always uses the maximum number of thinking tokens
- B. Claude dynamically decides when and how much to think; no token budget to tune
- C. It disables tool use
- D. It requires a separate beta header on every model

**A3.** On `claude-opus-4-8`, which sampling parameters are rejected with a 400?

- A. `max_tokens`
- B. `temperature`, `top_p`, and `top_k`
- C. `stop_sequences`
- D. `system`

**A4.** The cache write premium for a 5-minute TTL ephemeral cache is approximately:

- A. 0.1× base input price
- B. 1.25× base input price
- C. 2× base input price
- D. 10× base input price

**A5.** Cache **reads** cost approximately:

- A. 0.1× base input price
- B. 1.0× base input price
- C. 1.25× base input price
- D. Free

**A6.** With a 5-minute TTL, prompt caching breaks even after roughly how many requests
hitting the same prefix?

- A. 1
- B. 2
- C. 10
- D. 100

**A7.** A server-side tool loop hits its default iteration limit (10). The response
`stop_reason` will be:

- A. `end_turn`
- B. `max_tokens`
- C. `pause_turn`
- D. `refusal`

**A8.** To correctly resume after `pause_turn`, you should:

- A. Append a new user message saying "Continue."
- B. Re-send the user message + assistant response; the server resumes automatically
- C. Start a fresh conversation
- D. Switch to streaming

**A9.** Which is true about appending the assistant response in a manual tool loop?

- A. Append only the text, dropping `tool_use` blocks
- B. Append the full `response.content` (including `tool_use` blocks) before adding results
- C. Never append the assistant turn
- D. Append a summary string instead of the content

**A10.** Mid-conversation operator instructions that should preserve the cached prefix
are best delivered as:

- A. An edit to the top-level `system` field
- B. A `{"role": "system", ...}` message appended to `messages` (on supporting models)
- C. A new tool definition
- D. A `cache_control` change

**A11.** Editing the top-level `system` field mid-conversation will:

- A. Have no caching impact
- B. Invalidate the cached prefix ahead of the entire conversation
- C. Only invalidate the tools cache
- D. Return a 400

**A12.** The maximum number of `cache_control` breakpoints per request is:

- A. 1
- B. 4
- C. 16
- D. Unlimited

**A13.** A breakpoint walks backward at most how many content blocks to find a prior
cache entry?

- A. 4
- B. 10
- C. 20
- D. 100

**A14.** For structured outputs in Python, the recommended high-level helper that
validates the response against your schema is:

- A. `client.messages.create()` with manual `json.loads()`
- B. `client.messages.parse()`
- C. `client.messages.batches.create()`
- D. `client.beta.files.upload()`

**A15.** Which JSON Schema feature is **not** supported by structured outputs?

- A. `enum`
- B. `anyOf`
- C. Numerical constraints like `minimum`/`maximum`
- D. `additionalProperties: false`

**A16.** Compaction (beta) requires which critical handling on each turn?

- A. Stripping all thinking blocks
- B. Appending `response.content` (not just the text) back to messages
- C. Disabling tool use
- D. Resetting `max_tokens` to 0

**A17.** The Files API is most appropriate when you want to:

- A. Stream tokens to a UI
- B. Reference an uploaded document by `file_id` across multiple requests without re-uploading
- C. Cache the system prompt
- D. Run code server-side

**A18.** `tool_choice` set to `{"type": "any"}` means:

- A. Claude decides whether to use a tool (default)
- B. Claude must use at least one tool
- C. Claude must use one specific named tool
- D. Claude cannot use tools

**A19.** In Managed Agents, MCP server **credentials** are supplied via:

- A. The `mcp_servers` array on the agent (inline auth)
- B. A vault attached to the session via `vault_ids`
- C. The environment's networking config
- D. The session's `metadata`

**A20.** Which statement about Managed Agents archiving is correct?

- A. Archiving an agent is reversible
- B. Archiving an agent makes it read-only with no unarchive; new sessions can't reference it
- C. Sessions cannot be archived
- D. Archiving deletes all event history immediately

**A21.** A `limited` networking environment that declares MCP servers will silently fail
to reach them unless you:

- A. Set `allow_mcp_servers: true` or list the domains in `allowed_hosts`
- B. Switch the model to Opus
- C. Increase `max_tokens`
- D. Attach a second vault

**A22.** To pin a Managed Agent session to a known-good configuration for
reproducibility, you:

- A. Re-create the agent each run
- B. Pass `{type: "agent", id, version: N}` on session create
- C. Edit the environment
- D. Use a bare string `agent="agent_id"` (always latest)

**A23.** Which is the correct fallback strategy for a `claude-fable-5` request that may
be refused by safety classifiers, on the first-party API?

- A. There is no fallback mechanism
- B. The server-side `fallbacks` parameter with the `server-side-fallback-2026-06-01` beta
- C. Increasing `effort` to `max`
- D. Setting `temperature: 0`

**A24.** A `claude-fable-5` request from a zero-data-retention organization returns 400
on every call. The fix is:

- A. Add a `cache_control` block
- B. Adjust the org's data-retention configuration (Fable 5 needs 30-day retention)
- C. Reduce `max_tokens`
- D. Remove the `system` field

**A25.** Which `effort` level is the recommended best setting for most coding and
agentic use cases on Opus 4.7/4.8 and Fable 5?

- A. `low`
- B. `medium`
- C. `xhigh`
- D. `minimal`

---

## Section 2 — Multiple response (8 × 3 pts = 24 pts)

Select **all** correct options. No partial credit.

**B1.** Which changes invalidate **only** the system + messages caches but **not** the
tools cache? (Select all)

- A. Changing system prompt content
- B. Adding or removing a tool definition
- C. Switching the model
- D. Changing message content

**B2.** Which are appropriate uses of the manual agentic loop instead of the tool
runner? (Select all)

- A. Human-in-the-loop approval before each tool call
- B. Custom logging or conditional tool execution
- C. Per-token streaming with fine-grained control
- D. When you want the SDK to handle everything automatically

**B3.** Which are true about server-side tools? (Select all)

- A. Code execution runs in an Anthropic-hosted sandbox
- B. Web search returns results with citations
- C. They are declared in the `tools` array like other tools
- D. You must execute them client-side and return `tool_result`

**B4.** Which are valid reasons to choose Sonnet 4.6 over Opus 4.8? (Select all)

- A. Faster turnaround for high-volume workloads
- B. Lower per-token cost
- C. It is strictly more capable than Opus 4.8
- D. Adequate quality for many production tasks at better economics

**B5.** Which are true about token counting and tokenizers? (Select all)

- A. `tiktoken` undercounts Claude tokens and should not be used
- B. Token counts are model-specific
- C. Fable 5 uses the same tokenizer as Opus 4.8
- D. Coming from Opus 4.6 or older, token counts are identical to Fable 5

**B6.** Which are valid ways to retry a refused `claude-fable-5` request on another
model? (Select all)

- A. Server-side `fallbacks` parameter (first-party / Claude Platform on AWS)
- B. SDK client-side refusal-fallback middleware (incl. Bedrock/Vertex/Foundry)
- C. Hand-rolled retry on `claude-opus-4-8` re-sending the conversation
- D. Re-sending with `temperature: 2`

**B7.** Which are characteristics of Managed Agents sessions? (Select all)

- A. They reference a pre-created agent by ID
- B. They stream events back to the client
- C. They provision a container as the agent's tool-execution workspace
- D. They define the model and system prompt inline

**B8.** Which statements about `max_tokens` defaults are good practice? (Select all)

- A. Default ~16K for non-streaming requests to avoid HTTP timeouts
- B. Default ~64K for streaming requests since timeouts aren't a concern
- C. Use a small value like 256 for classification tasks
- D. Always set it to the model maximum regardless of task

---

## Section 3 — Scenario design (3 questions, ~8.6 pts each = 26 pts)

Answer in a few sentences each. Name specific features/parameters.

**C1. (Agent design)**
You're building a coding agent. Claude keeps spawning subagents for trivial single-file
reads, and overtriggers a tool because the prompt says `CRITICAL: You MUST use this
tool`. On Opus 4.8, what prompt and parameter changes would you make, and why?

**C2. (Context at scale)**
A research agent runs for hours across hundreds of tool calls and must retain learnings
across separate sessions. Describe which three context-management mechanisms you'd
combine and what each one does.

**C3. (Migration)**
A service currently calls `claude-opus-4-6` with
`thinking: {type: "enabled", budget_tokens: 8000}`, `temperature: 0.7`, and a final
assistant-turn prefill of `{"name": "`. You are migrating to `claude-opus-4-8`. List the
specific code changes required to avoid 400 errors and what replaces the prefill.

---

*End of Form B. Score with `answer-keys.md`.*
