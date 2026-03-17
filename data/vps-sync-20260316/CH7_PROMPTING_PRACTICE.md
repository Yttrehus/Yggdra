# Chapter 7: Prompt Engineering (and Why the Name Is Wrong)

**Written:** 2026-02-09
**Research base:** 2 complete agents + partial third — context engineering, anti-patterns, advanced patterns
**Sources:** 35+ papers, production reports, and practitioner analysis (cited inline)

---

## 7.1 The Name Change That Matters

In June 2025, Shopify CEO Tobi Lutke posted: "I really like the term 'context engineering' over prompt engineering. It describes the core skill better: the art of providing all the context for the task to be plausibly solvable by the LLM."

Andrej Karpathy co-signed immediately: "In every industrial-strength LLM app, context engineering is the delicate art and science of filling the context window with just the right information for the next step."

This wasn't branding. It was a correction. The actual skill had outgrown the name. Early prompting (2023) was about crafting the perfect instruction. Context engineering (2025+) is about assembling the right information environment — instructions, retrieved knowledge, conversation state, tool definitions, examples, and memory — so the model can succeed.

**The math:** The prompt itself might be 5% of the context window. The other 95% is scaffolding. If you're optimizing your instruction text while ignoring what documents get retrieved, what conversation history gets included, and how your tools are described, you're optimizing the wrong 5%.

Anthropic's own data: **54% better agent performance** through context engineering strategies versus prompt optimization alone.

---

## 7.2 The Hierarchy That Saves You Time

When prompt quality is bad, work through this hierarchy in order. Most problems are solved at level 1-2. Most people start at level 4.

| Level | Action | Effort | Impact |
|-------|--------|--------|--------|
| **1** | Fix the context (what information does the model see?) | Low | **Highest** |
| **2** | Fix the structure (XML tags, clear sections, examples) | Low | High |
| **3** | Fix the instruction (what you're asking for) | Low | Medium |
| **4** | Add evaluation (test cases, metrics, regression) | Medium | Medium |
| **5** | Optimize (meta-prompting, DSPy, A/B testing) | High | Low-Medium |
| **6** | Change the model | High | Variable |

**Context > instruction > structure > optimization > model.** That is the order. Level 1 solves 80% of problems. Level 5 solves the last 5%. Most of the blog posts are about level 5.

This is the Ladder applied to prompting.

---

## 7.3 The Anti-Pattern Hall of Fame

Most viral prompting techniques are superstition. The evidence base is thin, model-specific, or measures the wrong thing.

| Anti-Pattern | What People Think | What Actually Happens | Evidence |
|---|---|---|---|
| **"You are an expert in X"** | Makes the model smarter | Changes tone/vocabulary, not knowledge. No study proves it improves factual accuracy. | Adds confidence to hallucinations |
| **"Take a deep breath"** | Calms the AI | The "step by step" part helps (CoT). The breathing is noise. Found by another LLM optimizing PaLM 2 specifically. | DeepMind OPRO paper, model-specific |
| **"I'll tip you $200"** | Motivates quality | No significant quality improvement. Original study measured output *length*, not quality. | Woolf 2024, inconclusive K-S tests |
| **"This is very important"** | Increases effort | Emotional manipulation. Inconsistent effects at best. | No controlled studies |
| **"Think step by step" on simple tasks** | Improves everything | Adds latency + cost. Only helps multi-step reasoning. Oxford study: CoT *reduces* accuracy on certain tasks. | Use selectively, not universally |
| **500-word system prompts** | More instructions = more control | Dilutes signal. Model "forgets" buried instructions. | Less > more in production |
| **"Do NOT do X"** | Prevents behavior | Models are unreliable with negation. State what you WANT instead. | Anthropic docs confirm |
| **Copy prompts from Twitter** | Works for them = works for you | Model-specific, context-specific, version-specific | Almost never transfers |

### What Works Instead

**Show, don't tell.** One good example communicates more than three paragraphs of description. Few-shot examples consistently outperform elaborate instructions.

**Be direct.** Gemini's prompting guide: "Say the goal and the output format, then stop." The best production prompts are short, direct, and well-structured — not long and clever.

**Give context, not identity.** Instead of "You are an expert in X," provide examples of expert-level output. Show the code. Give the error message. Context > persona.

**Build eval first.** Define what "good" looks like before writing the prompt. Without evaluation criteria, you're optimizing by vibes.

---

## 7.4 What Actually Matters for Frontier Models (2026)

### Chain-of-Thought: Real but Overused

CoT genuinely helps on multi-step reasoning, math, and complex analysis. The evidence is robust. But:

- **Frontier models think by default.** Claude's adaptive thinking and GPT-4's internal reasoning make explicit "think step by step" increasingly unnecessary. The model already does it.
- **CoT hurts on simple tasks.** Oxford study showed CoT *reduces* accuracy on some tasks by overthinking simple problems. It adds latency and cost for zero benefit on classification, extraction, and formatting.
- **Use surgically:** Enable extended thinking for complex reasoning. Skip it for straightforward tasks.

### Few-Shot vs Zero-Shot

**Few-shot helps when:** Output format is non-obvious, domain has specialized conventions, you need consistent style across outputs, the task is classification with subtle categories.

**Zero-shot is enough when:** Frontier models (Claude Opus 4.6, GPT-4) already understand the task well. Simple extraction, summarization, or Q&A. Clear instructions make the expected output obvious.

**Diminishing returns:** 1-3 examples give most of the benefit. 5+ examples rarely improve quality further but eat context window. Quality of examples matters more than quantity.

### Structured Output

JSON mode, XML tags, schemas — these are the unsung heroes of production prompting.

**Why it matters:** Structured output eliminates the entire category of "parsing the model's response" failures. When you need JSON, don't hope for JSON — constrain to JSON.

**The hierarchy:** Schema-enforced (Anthropic Structured Outputs, OpenAI JSON mode) > XML tags with validation > markdown formatting > freeform with regex parsing.

---

## 7.5 Claude-Specific Patterns

Every model has idiosyncrasies. Claude's are documented. Using them is free performance.

### XML Tags for Structure

Claude is specifically trained to understand XML tags as structural markers. Not prompting advice — architecture advice.

```xml
<context>
{{retrieved_documents}}
</context>

<instructions>
Analyze the documents above and extract all customer complaints.
Return as JSON array.
</instructions>
```

**Why it works:** XML tags create unambiguous boundaries between instruction types. The model doesn't have to infer where context ends and instructions begin. Eliminates "the model mixed up my examples with my instructions."

### Extended Thinking / Adaptive Thinking

Claude Opus 4.6 uses adaptive thinking — dynamically decides when and how much to think. Controlled via `effort` parameter (low/medium/high/max), not manual `budget_tokens`.

**Choose when:** Complex reasoning, multi-step analysis, decisions needing auditability.
**Avoid when:** Simple extraction, formatting, classification. Adds latency for no gain.

### System Prompts Are Not Suggestions

Claude's system parameter sets persistent context for the entire conversation. This is where non-negotiable constraints go — not in the user message. Put nice-to-haves in user messages.

### Opus 4.6 Specific Notes

- **More proactive than previous models.** Dial back "CRITICAL: You MUST use this tool" language. Normal prompting works: "Use this tool when..."
- **Prefilling deprecated on last assistant turn.** Use Structured Outputs instead for format enforcement.
- **Tends to overengineer.** Add explicit "keep solutions simple" instructions if needed.
- **Strong parallel tool calling.** Will naturally parallelize unless told not to.

---

## 7.6 Multi-Turn: The Silent Killer

### The Number

**39% average accuracy drop** when the same task is delivered across multiple conversation turns instead of a single prompt. Tested across all major models — GPT-4 and Gemini 2.5 Pro show 30-40% drops. Worst case: 73% degradation with long prior context. (arxiv, May 2025)

Your carefully designed multi-turn workflow might perform *half as well* as batching all information into one message.

### Why It Happens

1. **Premature answering.** Models attempt solutions before having all information. First-20% turns: ~31% accuracy. Last-20% turns: ~64%.
2. **Assumption accumulation.** Model fills gaps with assumptions in early turns, treats them as facts later.
3. **Lost in the middle.** Information in middle turns gets less weight.
4. **Verbosity inflation.** Each turn adds noise. Code responses grow from ~700 to 1,400+ characters, with extra length being mostly incorrect.

### The Fix

**Consolidate before generate.** Collect information across turns, then batch into one clean prompt for final generation. The conversation collects; the generation starts fresh.

**Start fresh over sunk cost.** If quality degrades after 15+ turns, a new conversation with a good summary outperforms the degraded context. Don't fight sunk cost.

**Sliding window.** For long-running assistants: keep last N turns, summarize older ones.

---

## 7.7 Prompt Injection: The Permanent Problem

Prompt injection is #1 on OWASP's 2025 Top 10 for LLM Applications. Both the UK NCSC and OpenAI independently stated it **may never be fully solved.**

The reason is structural: unlike SQL injection (parameterized queries create a hard boundary), LLMs process instructions and data in the same token stream. No architectural separation exists.

### Direct vs Indirect

**Direct:** User types malicious instructions. Kevin Liu extracting Bing's "Sydney" system prompt in Feb 2023.

**Indirect:** Malicious instructions embedded in content the AI processes — web pages, code comments, documents. Four of five high-impact attacks in 2024-2025 are indirect. GitHub Copilot CVE-2025-53773: prompt injection in public repo code comments caused IDE settings modification enabling arbitrary code execution.

### Defense Reality

No complete defense exists. Practical mitigations:
- Least-privilege architectures (limit what the model can *do*)
- Human-in-the-loop for high-consequence actions
- Input/output filtering and guardrails
- Treating AI actions as untrusted input to downstream systems
- The two-way door principle: reversible actions = auto, irreversible = human gate

The fact that defenses are imperfect does not make them theater.

---

## 7.8 Prompts Are Code

The most underrated insight in production prompting: **prompts are code.** They need version control, regression tests, and migration strategies.

### The Brittleness Problem

NAACL 2025 research: LLMs exhibit high sensitivity to prompt format variations, even when semantic content is identical. Changing example order, adding spaces, swapping synonyms — all can shift performance.

**The migration problem:** A system on GPT-4 breaks when moving to GPT-4.1. Each model interprets prompts differently. Regression test pass rates dropped from 100% to 98% — sounds small until 2% of production requests fail silently.

### What Production Teams Do

- Version control prompts in Git alongside application code
- Regression test suites with expected outputs
- A/B testing with statistical significance thresholds
- Canary releases (10% traffic to new version, monitor, roll out)
- Treat model updates as breaking changes requiring re-validation

### The Anti-Pattern

Prompts stored in Slack threads and Notion pages. Changed without measuring impact. Discovered broken from user complaints. This is 2023-era practice. Production prompts in 2026 are versioned, tested, and monitored.

---

## 7.9 Prompt Composition — From Monolith to Modules

### The Three-Layer Architecture

```
[System Layer]   — Identity, constraints, formatting (always loaded)
[Domain Layer]   — Skill-specific knowledge, examples (loaded on trigger)
[Query Layer]    — Retrieved context, user input, state (dynamic per-turn)
```

**System layer** = CLAUDE.md. Changes rarely. Defines personality, constraints, the floor for quality.
**Domain layer** = Skills. Modular, version-controlled, testable in isolation.
**Query layer** = Everything assembled at runtime. RAG results, user message, conversation turns.

Miessler's 77-skill architecture is the clearest production example: each skill has a SKILL.md (routing), context files (domain knowledge), and Workflows (procedures). Only relevant skills load.

### Choose When / Avoid When

**Compose when:** Multiple use cases share common instructions, you need to test components independently, prompt exceeds ~500 words and you can't tell what affects what.

**Keep simple when:** One use case, one user, the prompt fits in your head.

---

## 7.10 Our Setup

**What we run:**
- **CLAUDE.md** (~200 lines, always loaded): Identity, 12 core frameworks, working principles, infrastructure map. Not a "prompt" — a persistent context layer.
- **5 skills** (loaded on trigger): route-lookup, webapp-dev, infrastructure, data-analysis, advisor. Only relevant skill loads, keeping context focused.
- **Qdrant vector search** (dynamic): `ctx "query" --limit 5` retrieves relevant chunks from 65K+ vectors. RAG providing query-specific context.
- **Research agent prompts** (meta-prompting): The 3-parallel-agent pattern used to write this book. Specific angles per agent, opinionated instructions, "Choose when / Avoid when" structure baked into the prompt.

**What we learned:**
- CLAUDE.md is the highest-leverage document in the entire system. 200 lines that shape every interaction. When we improved it, everything improved.
- Skills modularity prevents the "God Prompt" anti-pattern. When the advisor skill degrades, fix the advisor skill. Infrastructure skill is unaffected.
- Research agent prompts improved dramatically from Ch 3 → Ch 7. The Ch 3 prompts said "research everything about X." The Ch 7 prompts say "focus on insight over features, use Choose when / Avoid when, be opinionated." Constraint > freedom in prompting.
- The `ctx` command is context engineering in one line. 5 relevant chunks from 65K vectors, injected at query time. This single feature does more for quality than any prompt technique.

**What we'd do differently:** Version-controlled skill files with regression tests. Evaluation set for CLAUDE.md changes (does this edit improve or degrade typical interactions?). Track which skills load most often — probably over-engineering some, under-using others.

---

## Sources

### Context Engineering
- Tobi Lutke tweet (June 2025), Andrej Karpathy tweet (June 2025)
- Simon Willison, "Context Engineering" (June 2025)
- Anthropic: "Effective Context Engineering for AI Agents" — 54% improvement finding

### Anti-Patterns
- Yang et al., "Large Language Models as Optimizers" (DeepMind OPRO, 2023) — "take a deep breath"
- Max Woolf, "Does Offering ChatGPT a Tip Cause Better Text?" (2024) — inconclusive
- Bsharat et al., "Principled Instructions Are All You Need" (2023) — 26 principles

### Multi-Turn
- "LLMs Get Lost In Multi-Turn Conversation" (arxiv, May 2025) — 39% drop
- JetBrains Research: "Smarter Context Management" (Dec 2025)

### Prompt Injection
- OWASP Top 10 for LLM Applications (2025)
- UK NCSC: "Prompt Injection Is Not SQL Injection"
- GitHub Copilot CVE-2025-53773, Cursor IDE CVE-2025-54135/54136
- Miessler: "Is Prompt Injection a Vulnerability?" (2025)

### Production & Optimization
- DSPy Framework (Stanford, 160K monthly downloads)
- NAACL 2025: "Towards LLMs Robustness to Changes in Prompt Format Styles"
- Anthropic: XML tags, adaptive thinking, Opus 4.6 best practices

### Prompt Composition
- Miessler: "When to Use Skills vs Commands vs Agents"
- Langfuse: "Prompt Composability" (March 2025)

---

**Word count:** ~2,600 words (~400 lines)
**Status:** Chapter complete
